# GA Robot - Hệ Thống Tối Ưu Lộ Trình Giao Hàng

## Giới Thiệu

GA Robot là ứng dụng web giúp tối ưu hóa lộ trình giao hàng bằng thuật toán Genetic Algorithm. Người dùng có thể chọn các điểm giao hàng trực tiếp trên bản đồ, hệ thống sẽ tính toán lộ trình tối ưu nhất và hiển thị trên bản đồ tương tác với đường đi thực tế.

## Tính Năng Chính

Ứng dụng cung cấp giao diện trực quan với bản đồ tương tác cho phép người dùng click để thêm các điểm giao hàng. Khi nhấn nút Chạy Genetic Algorithm, hệ thống sẽ tối ưu lộ trình và hiển thị kết quả bao gồm tổng khoảng cách, thứ tự giao hàng, và khoảng cách từng đoạn. Ứng dụng hỗ trợ hiệu ứng loading, thông báo lỗi chuyên nghiệp, và xóa tất cả điểm để bắt đầu lại.

## Công Nghệ Sử Dụng

Backend được xây dựng bằng Flask phiên bản 3.1.3, một framework web nhẹ và linh hoạt cho Python. Frontend sử dụng Bootstrap 5.3.3 để xây dựng giao diện đáp ứng với chủ đề tối hiện đại. Bản đồ tương tác được cấp bởi Leaflet phiên bản 1.9.4 kết hợp với dữ liệu tile từ OpenStreetMap. Định tuyến đường thực tế được lấy từ OSRM Open Source Routing Machine API.

## Yêu Cầu Hệ Thống

Python phiên bản 3.10 trở lên là bắt buộc để chạy ứng dụng. Các gói Python cần thiết được liệt kê trong file requirements.txt. Trình duyệt hiện đại hỗ trợ HTML5 và JavaScript ES6 là cần thiết để sử dụng giao diện web.

## Cách Cài Đặt

Đầu tiên, clone hoặc copy toàn bộ thư mục dự án đến máy tính của bạn. Mở Terminal hoặc PowerShell và điều hướng đến thư mục gốc của dự án. Tạo virtual environment bằng lệnh python -m venv .venv. Kích hoạt virtual environment bằng lệnh .venv\Scripts\Activate.ps1 trên Windows hoặc source .venv/bin/activate trên Linux/Mac. Cài đặt các gói phụ thuộc bằng lệnh pip install -r requirements.txt.

## Hướng Dẫn Sử Dụng

Điều hướng vào thư mục robot bằng lệnh cd robot. Chạy ứng dụng bằng lệnh python app.py. Mở trình duyệt web và truy cập địa chỉ http://127.0.0.1:5050. Trên bản đồ, nhấp chuột để thêm các điểm giao hàng. Điểm đầu tiên sẽ được đánh dấu là kho P0 với màu đỏ, các điểm khác có màu xanh. Sau khi chọn ít nhất 3 điểm, nhấn nút Chạy Genetic Algorithm để tính toán lộ trình tối ưu. Kết quả sẽ hiển thị số lượng điểm, tổng khoảng cách, thứ tự giao hàng, và khoảng cách từng đoạn. Đường giao hàng tối ưu sẽ được vẽ trên bản đồ với các màu khác nhau cho từng đoạn đường. Để bắt đầu lại, nhấn nút Xóa tất cả điểm.

## Cấu Trúc Dự Án

Thư mục robot chứa file app.py là backend chính của ứng dụng. Thư mục templates chứa file index.html là giao diện chính. Thư mục static chứa file styles.css cho định kiểu giao diện và file app.js cho logic phía client. File requirements.txt liệt kê các gói Python cần cài đặt. File test.py là file test cho phát triển.

## Chi Tiết Thuật Toán

Genetic Algorithm được sử dụng với dân số ban đầu là 100 cá thể, chạy 200 thế hệ. Mỗi cá thể đại diện cho một lộ trình khác nhau. Hàm fitness tính tổng khoảng cách của mỗi lộ trình. Quá trình lựa chọn sử dụng giải đấu với kích thước 5 để chọn ra những cá thể tốt nhất. Crossover sao chép một đoạn từ cá thể cha mẹ thứ nhất và điền phần còn lại từ cá thể cha mẹ thứ hai. Mutation thay đổi ngẫu nhiên vị trí của hai điểm với xác suất 20%. Năm cá thể tốt nhất từ mỗi thế hệ được bảo toàn sang thế hệ tiếp theo.

## API Backend

Ứng dụng cung cấp endpoint POST tại đường dẫn /optimize. Request phải gửi JSON chứa mảng điểm với tọa độ kinh độ vĩ độ. Response trả về JSON chứa best_route là mảng thứ tự giao hàng tối ưu, best_distance là tổng khoảng cách tính bằng mét, points_count là số lượng điểm, và route_distances là mảng khoảng cách từng đoạn.

## Giao Diện Người Dùng

Giao diện được thiết kế với chủ đề tối hiện đại sử dụng các màu xanh lá cây cho accent chính và xanh dương cho accent phụ. Header chứa logo GA Robot và các liên kết điều hướng. Hero card giới thiệu ứng dụng và hiển thị số lượng điểm đã chọn. Panel bên trái cung cấp các nút điều khiển để chạy GA và xóa điểm, cùng với khu vực hiển thị kết quả. Bản đồ tương tác chiếm 2/3 chiều rộng màn hình để dễ dàng chọn điểm và xem kết quả.

## Thông Báo và Xử Lý Lỗi

Khi người dùng cố gắng chạy GA mà chưa chọn đủ 3 điểm, một modal thông báo sẽ hiển thị với thông điệp rõ ràng. Nếu có lỗi khi gọi API OSRM để lấy đường thực tế, hệ thống sẽ tự động sử dụng đường thẳng giữa hai điểm thay thế. Các lỗi từ server sẽ được hiển thị trong khu vực kết quả dưới dạng thông báo lỗi.

## Tối Ưu Hóa Hiệu Năng

Phần vẽ đường trên bản đồ được thực hiện không đồng bộ để không làm treo giao diện. Hình ảnh tile bản đồ được cache bởi trình duyệt. API OSRM có timeout 8 giây để tránh chờ quá lâu. Request được gửi riêng cho từng đoạn đường song song để tận dụng tối đa năng lực.

## Phát Triển Thêm

Để thêm tính năng mới, chỉnh sửa file app.py cho backend hoặc file app.js cho frontend. Mỗi lần thay đổi code Python, server sẽ tự động reload nhờ debug mode. Đối với JavaScript, nhấn Ctrl+Shift+R trong trình duyệt để clear cache và tải phiên bản mới.

## Giấy Phép

Dự án này được phát triển cho mục đích học tập và sử dụng nội bộ. Vui lòng tham khảo các tệp giấy phép của các thư viện bên thứ ba được sử dụng.

## Liên Hệ và Hỗ Trợ

Nếu gặp bất kỳ vấn đề nào hoặc có đề xuất cải tiến, vui lòng liên hệ với nhóm phát triển dự án.
