# Web Scraper cho Balocenter

## Mô tả chi tiết

Dự án này bao gồm một bộ công cụ Python được thiết kế để tự động thu thập (scrape) và xử lý thông tin sản phẩm từ trang web thương mại điện tử `https://balocenter.com/collections/all`. Mục tiêu chính là trích xuất các thuộc tính quan trọng của mỗi sản phẩm được liệt kê trên trang, bao gồm nhưng không giới hạn ở:

*   **Nhà cung cấp (Vendor):** Thương hiệu hoặc nhà sản xuất của sản phẩm. Thông tin này giúp phân loại và nhận diện nguồn gốc của sản phẩm.
*   **Tên sản phẩm (Title):** Tên đầy đủ và chính xác của sản phẩm như được hiển thị trên website.
*   **Giá gốc (Original Price):** Giá niêm yết ban đầu của sản phẩm trước khi áp dụng bất kỳ chương trình khuyến mãi nào.
*   **Giá bán (Sale Price):** Giá thực tế mà khách hàng phải trả sau khi đã áp dụng các chương trình giảm giá hoặc khuyến mãi (nếu có).
*   **URL hình ảnh (Image URL):** Đường dẫn trực tiếp đến hình ảnh đại diện chất lượng cao của sản phẩm. Hình ảnh này có thể được sử dụng cho mục đích hiển thị hoặc lưu trữ.
*   **URL sản phẩm (Product URL):** Đường dẫn duy nhất (permalink) đến trang chi tiết của sản phẩm trên website `balocenter.com`.

Sau khi quá trình thu thập hoàn tất, dữ liệu thô sẽ được xử lý, làm sạch và cấu trúc lại. Kết quả cuối cùng được lưu trữ dưới nhiều định dạng tệp phổ biến (CSV, Excel, SQL dump) để đảm bảo tính linh hoạt và thuận tiện cho các mục đích sử dụng khác nhau như phân tích dữ liệu, báo cáo, hoặc tích hợp vào các hệ thống quản lý cơ sở dữ liệu.

## Cấu trúc dự án

Dự án bao gồm các tệp chính sau:

*   **`crawl_data.py`**: Script chính thu thập dữ liệu và lưu vào `products.csv`.
*   **`crawl_data_excel.py`**: Script thu thập dữ liệu và lưu trực tiếp vào `products.xlsx`.
*   **`crawl_data.ipynb`**: Jupyter Notebook minh họa quá trình thu thập dữ liệu.
*   **`products.csv`**: Dữ liệu sản phẩm ở định dạng CSV.
*   **`products.xlsx`**: Dữ liệu sản phẩm ở định dạng Excel.
*   **`product_db_dump.sql`**: SQL dump để nhập dữ liệu vào cơ sở dữ liệu.

## Hướng dẫn chạy script

Để chạy script thu thập dữ liệu, vui lòng thực hiện theo các bước sau:

### 1. Điều kiện cần có

* Đã cài đặt Python phiên bản 3.x trở lên trên máy tính của bạn.
* Các thư viện Python sau: 
  * `requests` để gửi yêu cầu HTTP
  * `beautifulsoup4` để phân tích cú pháp HTML
  * `openpyxl` để làm việc với file Excel (nếu muốn sử dụng script crawl_data_excel.py)
  * `pandas` để xử lý dữ liệu (nếu chạy notebook)

### 2. Cài đặt các thư viện cần thiết

Mở terminal (hoặc command prompt) và chạy lệnh sau để cài đặt các thư viện cơ bản:

```bash
pip install requests beautifulsoup4
```

Nếu muốn sử dụng tất cả các tính năng trong dự án, hãy cài đặt đầy đủ các thư viện:

```bash
pip install requests beautifulsoup4 pandas openpyxl jupyter
```

### 3. Thực thi các script

#### Script cơ bản (crawl_data.py)

* Di chuyển đến thư mục chứa mã nguồn:
  ```bash
  cd path/to/your/project/src
  ```
* Chạy script cơ bản:
  ```bash
  python crawl_data.py
  ```
* Script sẽ thu thập dữ liệu từ trang web và lưu vào file `products.csv`

#### Script Excel (crawl_data_excel.py)

* Chạy script để lưu trữ dữ liệu vào file Excel:
  ```bash
  python crawl_data_excel.py
  ```
* Dữ liệu sẽ được lưu vào file `products.xlsx` với các định dạng và công thức tự động

#### Jupyter Notebook (crawl_data.ipynb)

* Khởi chạy Jupyter notebook:
  ```bash
  jupyter notebook
  ```
* Mở file `crawl_data.ipynb` trong trình duyệt
* Thực thi từng cell trong notebook để xem quá trình thu thập và phân tích dữ liệu với các giải thích chi tiết

### 4. Nhập dữ liệu vào cơ sở dữ liệu (tùy chọn)

Nếu bạn muốn nhập dữ liệu sản phẩm vào cơ sở dữ liệu MySQL/MariaDB:

```bash
mysql -u username -p database_name < product_db_dump.sql
```

## Các thư viện phụ thuộc

Dự án này sử dụng các thư viện và module Python sau:

* **requests:** Thực hiện các yêu cầu HTTP đến trang web `balocenter.com` và lấy nội dung HTML của các trang sản phẩm.
* **beautifulsoup4:** Phân tích (parse) nội dung HTML thu được từ `requests`. Thư viện này giúp dễ dàng trích xuất các thông tin cụ thể từ cấu trúc HTML của trang web.
* **csv:** Module tích hợp sẵn trong Python, được sử dụng để ghi dữ liệu đã thu thập vào tệp `products.csv` theo định dạng CSV (Comma-Separated Values).
* **time:** Module tích hợp sẵn, được sử dụng để tạo một khoảng dừng nhỏ (delay) giữa các yêu cầu HTTP. Điều này giúp tránh việc gửi quá nhiều yêu cầu liên tục đến máy chủ, có thể dẫn đến việc bị chặn IP hoặc gây quá tải cho server.
* **pandas (trong Jupyter Notebook):** Thư viện mạnh mẽ cho thao tác và phân tích dữ liệu. Trong notebook, `pandas` được sử dụng để tạo DataFrame, giúp dễ dàng xem, làm sạch và thực hiện các phép biến đổi trên dữ liệu thu thập được.
* **openpyxl (cho crawl_data_excel.py):** Thư viện cho phép đọc và ghi các tệp Excel 2010 xlsx/xlsm/xltx/xltm. Được sử dụng trong script `crawl_data_excel.py` để tạo và lưu trữ dữ liệu vào tệp `products.xlsx`.
* **jupyter (cho crawl_data.ipynb):** Nền tảng để chạy Jupyter Notebook, cung cấp một môi trường tương tác để viết và thực thi mã Python, kèm theo văn bản markdown và trực quan hóa.