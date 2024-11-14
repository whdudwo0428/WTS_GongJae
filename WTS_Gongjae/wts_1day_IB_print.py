import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 팔레트 클래스 정의
class Pallet:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width

# KS 표준 규격인 T11형 팔레트 정의
PLT_T11 = Pallet('T11', 1100, 1100)


# 상품 클래스 정의
class Product:
    def __init__(self, name, weight, length, width, height, items_per_pallet):
        self.name = name
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.items_per_pallet = items_per_pallet


# 상품 리스트 생성
products = []
min_items_per_pallet = 40
base_items_per_pallet = 200
for i in range(26):
    name = chr(97 + i)  # 'a'부터 'z'까지의 상품 이름
    weight = None  # 무게는 pass
    length = 110 + (i * 5)  # 가로 길이 조정 (예시)
    width = 110 + (i * 5)  # 세로 길이 조정 (예시)
    height = 100  # 높이 (예시)

    # 최소 40 이상의 아이템이 팔레트에 적재될 수 있도록 조정
    items_per_pallet = max(base_items_per_pallet - (i * 10), min_items_per_pallet)
    products.append(Product(name, weight, length, width, height, items_per_pallet))

# 상품 정보 출력
for product in products:
    print(f'상품명: {product.name}, 팔레트당 상품 개수: {product.items_per_pallet}')


# 창고 클래스 정의
class Warehouse:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zones = {}

    def add_zone(self, name, x, y, width, height):
        self.zones[name] = {'x': x, 'y': y, 'width': width, 'height': height}

    def plot_warehouse(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        for zone, dim in self.zones.items():
            rect = patches.Rectangle((dim['x'], dim['y']), dim['width'], dim['height'], linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            plt.text(dim['x'] + dim['width']/2, dim['y'] + dim['height']/2, zone, ha='center', va='center')
        plt.show()

# 창고 생성 및 구역 추가
warehouse = Warehouse(200, 100)
warehouse.add_zone('입고', 0, 75, 40, 25)
warehouse.add_zone('출고', 0, 0, 40, 25)
warehouse.add_zone('허브검수', 100, 25, 40, 50)

# 저장소 클래스 정의
class StorageArea:
    def __init__(self, name):
        self.name = name
        self.capacity = 20  # 최대 20 PLT로 제한
        self.current_stock = 0
        self.ea_per_plt = {}

    def update_stock(self, product, plt_amount, ea_amount):
        if product.name in self.ea_per_plt:
            self.ea_per_plt[product.name] += ea_amount
        else:
            self.ea_per_plt[product.name] = ea_amount
        self.current_stock += plt_amount

    def display_stock(self):
        print(f'적재구역 {self.name} 현재 재고 상태:')
        for product, ea in self.ea_per_plt.items():
            print(f'상품명: {product}, 팔레트 수: {self.current_stock}/{self.capacity} PLT, 개수: {ea}EA')
        print()

# 피킹 구현을 위한 토트 클래스 정의
class Tote:
    def __init__(self, code):
        self.code = code
        self.items = {}
        self.capacity = 100  # 예시 적재 용량 (pass)
        self.volume = 0  # 적재 부피

    def add_item(self, product, quantity):
        if product.name in self.items:
            self.items[product.name] += quantity
        else:
            self.items[product.name] = quantity
        self.volume += product.length * product.width * product.height * quantity

    def display_contents(self):
        print(f'Tote {self.code} 내용물:')
        for item, quantity in self.items.items():
            print(f'상품명: {item}, 개수: {quantity}')
        print()
# 테스트 예시

# 창고 시각화
warehouse.plot_warehouse()

# 상품 PLT당 적재개수 정보 출력
# 상품 정보 출력 함수 정의
def print_product_info(products):
    header = f"{'상품명':^5} {'상품 개수':^10} {'단위':^6}"
    separator = "="*38
    print(header)
    print(separator)
    for product in products:
        print(f"{product.name:^7} {product.items_per_pallet:^13} {'EA/PLT':^6}")
    print()
# 상품 정보 출력
print_product_info(products)

# 저장소 예시
storage_area = StorageArea('A')
product_a = products[0]
storage_area.update_stock(product_a, 16, 1934)
storage_area.display_stock()

# 토트 예시
tote_1 = Tote('00001')
tote_1.add_item(product_a, 3)
tote_1.display_contents()
