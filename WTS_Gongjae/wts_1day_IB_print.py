import csv
import pygame
import random

# 초기 pygame 설정
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Warehouse Simulation")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 기본 폰트 설정
font = pygame.font.Font(None, 24)


# 1. Pallet (PLT) 클래스
class Pallet:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width


# KS 표준 규격인 T11형 팔레트 정의
PLT_T11 = Pallet('T11', 1100, 1100)


# 2. Product 클래스 정의
class Product:
    def __init__(self, name, unit_volume, max_plt_capacity):
        self.name = name
        self.unit_volume = unit_volume  # 상품의 단위 부피
        self.max_plt_capacity = max_plt_capacity  # PLT당 최대 적재 가능한 개수
        self.total_quantity = random.randint(500, 1000)  # 초기 재고 설정
        self.current_plt = (self.total_quantity // max_plt_capacity) + (
            1 if self.total_quantity % max_plt_capacity else 0)

    def add_stock(self, quantity):
        self.total_quantity += quantity
        self.current_plt = (self.total_quantity // self.max_plt_capacity) + (
            1 if self.total_quantity % self.max_plt_capacity else 0)
        print(f"상품명: {self.name}, 팔레트 수: {self.current_plt}/20 PLT, 개수: {self.total_quantity} EA")

    def remove_stock(self, quantity):
        if self.total_quantity >= quantity:
            self.total_quantity -= quantity
            self.current_plt = (self.total_quantity // self.max_plt_capacity) + (
                1 if self.total_quantity % self.max_plt_capacity else 0)
        else:
            print(f"Not enough stock of {self.name}")
        print(f"상품명: {self.name}, 팔레트 수: {self.current_plt}/20 PLT, 개수: {self.total_quantity} EA")


# 3. Tote 클래스 정의 (25개 제한)
class Tote:
    tote_counter = 1  # 토트 ID 생성기

    def __init__(self):
        self.code = f"{Tote.tote_counter:05d}"
        Tote.tote_counter += 1
        self.items = {}
        self.max_capacity = 25  # 최대 25개까지 적재 가능

    def add_item(self, product, quantity):
        if product.name in self.items:
            if self.items[product.name] + quantity <= self.max_capacity:
                self.items[product.name] += quantity
            else:
                print(f"Tote {self.code} 내용물:")
                for name, qty in self.items.items():
                    print(f"상품명: {name}, 개수: {qty}")
                remaining = quantity - (self.max_capacity - self.items[product.name])
                self.items[product.name] = self.max_capacity
                print(f"새로운 토트에 {remaining}개 추가 필요.")
                return Tote()  # 새 토트 반환
        else:
            self.items[product.name] = min(quantity, self.max_capacity)
        print(f"Tote {self.code} 내용물:")
        for name, qty in self.items.items():
            print(f"상품명: {name}, 개수: {qty}")
        return self  # 현재 토트 반환


# 4. Warehouse 클래스 정의
class Warehouse:
    def __init__(self):
        self.products = self.create_products()
        self.totes = []

    def create_products(self):
        """26개의 상품 생성 및 등록"""
        products = {}
        for i in range(26):
            name = chr(97 + i)  # 상품명 a ~ z
            unit_volume = (i + 1) * 10  # 임의로 부피 설정
            max_plt_capacity = max(50, 200 - (i * 5))  # PLT당 최대 적재량
            products[name] = Product(name, unit_volume, max_plt_capacity)
        return products

    def stock_in(self, product_name, quantity):
        if product_name in self.products:
            self.products[product_name].add_stock(quantity)

    def stock_out(self, product_name, quantity):
        if product_name in self.products:
            self.products[product_name].remove_stock(quantity)

    def display_stock(self):
        print(f'적재구역 현재 재고 상태:')
        for name, product in self.products.items():
            print(f"상품명: {name.upper()}, 팔레트 수: {product.current_plt}/20 PLT, 개수: {product.total_quantity} EA")

    def draw_warehouse(self):
        """창고를 화면에 그립니다."""
        screen.fill(WHITE)
        x, y = 50, 50
        for i, (name, product) in enumerate(self.products.items()):
            # 상품 박스 그리기
            pygame.draw.rect(screen, GRAY, (x, y, 100, 80))
            # 상품명과 재고 표시
            text = font.render(f"{name.upper()}: {product.total_quantity}EA, {product.current_plt}PLT", True, BLACK)
            screen.blit(text, (x + 5, y + 5))
            # +, - 버튼 그리기
            plus_button = pygame.draw.rect(screen, GREEN, (x, y + 50, 30, 20))
            minus_button = pygame.draw.rect(screen, RED, (x + 70, y + 50, 30, 20))
            screen.blit(font.render('+', True, BLACK), (x + 10, y + 53))
            screen.blit(font.render('-', True, BLACK), (x + 75, y + 53))
            # 버튼에 대한 이벤트 처리
            if event.type == pygame.MOUSEBUTTONDOWN:
                if plus_button.collidepoint(event.pos):
                    self.stock_in(name, 100)  # 재고 +100
                elif minus_button.collidepoint(event.pos):
                    self.stock_out(name, 50)  # 재고 -50
            x += 120
            if (i + 1) % 6 == 0:
                x = 50
                y += 120


# 인스턴스 생성
warehouse = Warehouse()
tote1 = Tote()

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 예시: 입고/출고 작업 및 토트에 적재
    tote1 = tote1.add_item(warehouse.products["a"], 3)  # 재고가 초과될 경우 새 토트 생성

    # 재고 출력
    warehouse.display_stock()

    # 시각화 그리기
    warehouse.draw_warehouse()
    pygame.display.flip()
    clock.tick(10)  # FPS 설정

pygame.quit()
