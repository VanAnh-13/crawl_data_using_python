import requests
from bs4 import BeautifulSoup
import csv
import time


# Hàm để cào dữ liệu từ một trang
def crawl_page(url):
    # Headers để giả lập trình duyệt
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Gửi yêu cầu HTTP
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Không thể truy cập {url}, mã trạng thái: {response.status_code}")
        return []

    # Phân tích HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả sản phẩm
    products = soup.select('div.item.item-product.product-resize')
    if not products:
        print(f"Không tìm thấy sản phẩm nào trên {url}")
        return []

    # Danh sách lưu dữ liệu
    data = []

    # Trích xuất thông tin từ mỗi sản phẩm
    for product in products:
        # Lấy nhà cung cấp (vendor)
        vendor = product.find('div', class_='vendor')
        vendor_text = vendor.text.strip() if vendor else 'N/A'

        # Lấy tiêu đề (title)
        title_tag = product.find('span', class_='title')
        title = title_tag.find('a').text.strip() if title_tag and title_tag.find('a') else 'N/A'

        # Lấy giá gốc và giá khuyến mãi
        currency_sign = product.find('span', class_='currency-sign')
        original_price = currency_sign.find('del').text.strip() if currency_sign and currency_sign.find(
            'del') else 'N/A'
        sale_price = currency_sign.find('a').text.strip() if currency_sign and currency_sign.find('a') else 'N/A'

        # Lấy URL hình ảnh
        image_tag = product.find('div', class_='image')
        image = image_tag.find('a').find('img')['src'] if image_tag and image_tag.find('a') and image_tag.find(
            'a').find('img') else 'N/A'

        # Lấy URL sản phẩm
        product_url = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else 'N/A'
        if product_url and not product_url.startswith('http'):
            product_url = f"https://balocenter.com{product_url}"

        # Thêm dữ liệu vào danh sách
        data.append({
            'Vendor': vendor_text,
            'Title': title,
            'Original Price': original_price,
            'Sale Price': sale_price,
            'Image URL': image,
            'Product URL': product_url
        })

    return data


# Hàm chính để cào toàn bộ trang web
def main():
    base_url = 'https://balocenter.com/collections/all'
    all_data = []
    page = 1

    while True:
        # Tạo URL cho từng trang
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page}"

        print(f"Đang cào trang: {url}")

        # Cào dữ liệu từ trang hiện tại
        page_data = crawl_page(url)
        if not page_data:
            break  # Dừng nếu không còn dữ liệu

        # Thêm dữ liệu vào danh sách tổng
        all_data.extend(page_data)

        # Tăng số trang và đợi để tránh bị chặn
        page += 1
        time.sleep(1)  # Đợi 1 giây giữa các yêu cầu

    # Lưu dữ liệu vào file CSV
    if all_data:
        with open('products.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Vendor', 'Title', 'Original Price', 'Sale Price', 'Image URL',
                                                      'Product URL'])
            writer.writeheader()
            writer.writerows(all_data)
        print(f"Đã lưu {len(all_data)} sản phẩm vào file 'products.csv'")
    else:
        print("Không có dữ liệu nào được cào.")


# Chạy chương trình
if __name__ == "__main__":
    main()