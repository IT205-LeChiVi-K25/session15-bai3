# (1) Phân tích và thiết kế giải pháp

# Sơ đồ luồng dữ liệu (Data Flow Logic):
# [main()] ──► (Nhập thông tin) ──► [calculate_ticket_fare()] ──► (Trả về final_total) ──► [main()] ──► (Truyền final_total) ──► [process_booking()]
# Giải thích tính toàn vẹn dữ liệu (Data Integrity):
# - Biến 'flight_revenue' và 'available_seats' bắt buộc phải là biến toàn cục (Global Variables). 
# - Lý do: Hệ thống vận hành liên tục qua nhiều lượt giao dịch đặt vé và hủy vé khác nhau. Dữ liệu tài chính 
#   và số lượng ghế cần phải được lưu trữ tập trung tại một vùng nhớ duy nhất để tất cả các hàm nghiệp vụ 
#   (Đặt vé, Hủy vé, Báo cáo) đều có thể truy cập, cập nhật đồng bộ theo thời gian thực. Nếu sử dụng biến cục bộ 
#   (Local), dữ liệu sẽ bị giải phóng và xóa sạch ngay sau khi hàm kết thúc, gây mất mát dữ liệu của hệ thống.

# Định nghĩa các hằng số và biến toàn cục của hệ thống
MAX_CAPACITY = 50
BASE_PRICE = 2000.0

available_seats = 50
flight_revenue = 0.0

def calculate_ticket_fare(quantity, ticket_class):
    """
    Tính toán chi tiết giá vé máy bay dựa trên số lượng và hạng ghế lựa chọn.
    
    Tham số:
    quantity (int): Số lượng vé máy bay khách hàng muốn đặt (phải > 0).
    ticket_class (int): Hạng vé lựa chọn (1: Economy, 2: Business).
    
    Giá trị trả về:
    float: Tổng số tiền cuối cùng cần thanh toán sau khi tính phí dịch vụ sân bay 5%.
    """
    if ticket_class == 1:
        class_name = "Economy"
        unit_price = BASE_PRICE
    else:
        class_name = "Business"
        unit_price = BASE_PRICE * 1.5
        
    subtotal = quantity * unit_price
    airport_fee = subtotal * 0.05
    final_total = subtotal + airport_fee
    
    print("-> Xác nhận đặt chỗ:")
    print(f"Số lượng: {quantity} | Hạng: {class_name}")
    print(f"Tạm tính: ${subtotal:.1f}")
    print(f"Phí dịch vụ (5%): ${airport_fee:.1f}")
    print(f"Tổng thanh toán: ${final_total:.1f}")
    
    return final_total

def process_booking(quantity, total_fare):
    """
    Xử lý kiểm tra số lượng ghế trống và thực hiện trừ ghế, cộng doanh thu toàn cục.
    
    Tham số:
    quantity (int): Số lượng vé khách hàng đặt mua.
    total_fare (float): Tổng số tiền khách hàng cần thanh toán cho lượt đặt vé.
    """
    global available_seats, flight_revenue
    
    if quantity > available_seats:
        print(f"Rất tiếc, chuyến bay chỉ còn {available_seats} chỗ trống.")
        return False
        
    available_seats -= quantity
    flight_revenue += total_fare
    print(f"Đặt vé thành công! Ghế trống còn lại: {available_seats}")
    return True

def process_refund(quantity):
    """
    Xử lý hủy vé đã đặt và tính toán số tiền hoàn lại theo chính sách của hãng.
    
    Tham số:
    quantity (int): Số lượng vé khách hàng muốn yêu cầu hủy.
    """
    global available_seats, flight_revenue
    
    # Bẫy lỗi hủy khống vé (Ghost Refund)
    if available_seats + quantity > MAX_CAPACITY:
        print("Lỗi: Số lượng vé hủy vượt quá số vé đã bán ra.")
        return
        
    # Chính sách: hoàn 80% giá vé cơ bản, không hoàn phí dịch vụ
    refund_amount = quantity * (BASE_PRICE * 0.8)
    
    available_seats += quantity
    flight_revenue -= refund_amount
    
    print("Hủy vé thành công.")
    print(f"Hệ thống đã hoàn lại: ${refund_amount:.1f} (80% giá cơ bản).")
    print(f"Ghế trống hiện tại: {available_seats}")

def print_flight_report():
    """
    Xuất báo cáo trực quan về tình trạng vận hành và doanh thu hiện tại của chuyến bay VN2026.
    
    Định dạng báo cáo:
    --- TÌNH TRẠNG CHUYẾN BAY VN2026 ---
    Sức chứa tối đa: [Số nguyên]
    Ghế đã đặt: [Số nguyên]
    Ghế trống: [Số nguyên]
    Tổng doanh thu hiện tại: $[Số thập phân với 1 chữ số sau dấu phẩy]
    """
    booked_seats = MAX_CAPACITY - available_seats
    print("--- TÌNH TRẠNG CHUYẾN BAY VN2026 ---")
    print(f"Sức chứa tối đa: {MAX_CAPACITY}")
    print(f"Ghế đã đặt: {booked_seats}")
    print(f"Ghế trống: {available_seats}")
    print(f"Tổng doanh thu hiện tại: ${flight_revenue:.1f}")

def main():
    while True:
        print("============= SKYBOOKING SYSTEM =============")
        print("Chuyến bay: VN2026 | Khởi hành: Hà Nội")
        print("1. Đặt vé máy bay\n"
              "2. Hủy vé & Hoàn tiền\n"
              "3. Xem tình trạng chuyến bay\n"
              "4. Đóng hệ thống")
        print("=============================================")
        
        choice = input("Chọn chức năng (1-4): ").strip()
        
        match choice:
            case "1":
                print("\n--- ĐẶT VÉ MÁY BAY ---")
                str_qty = input("Nhập số lượng vé: ").strip()
                
                if not str_qty.isdigit():
                    print("Lỗi: Số lượng vé phải là số nguyên dương hợp lệ!")
                    print()
                    continue
                    
                quantity = int(str_qty)
                if quantity <= 0:
                    print("Lỗi: Số lượng vé đặt mua phải lớn hơn 0.")
                    print()
                    continue
                    
                # Kiểm tra nhanh lỗi Overbooking trước khi xử lý hạng ghế
                if quantity > available_seats:
                    print(f"Rất tiếc, chuyến bay chỉ còn {available_seats} chỗ trống.")
                    print()
                    continue
                    
                ticket_class = input("Chọn hạng vé (1: Economy, 2: Business): ").strip()
                if ticket_class not in ["1", "2"]:
                    print("Lỗi: Hạng vé không hợp lệ! Chỉ chọn 1 hoặc 2.")
                    print()
                    continue
                    
                ticket_class = int(ticket_class)
                
                # Chạy luồng dữ liệu tính toán chi phí và thực thi nghiệp vụ đặt vé
                total_fare = calculate_ticket_fare(quantity, ticket_class)
                process_booking(quantity, total_fare)
                print()
                
            case "2":
                print("\n--- HỦY VÉ & HOÀN TIỀN ---")
                str_refund_qty = input("Nhập số lượng vé muốn hủy: ").strip()
                
                if not str_refund_qty.isdigit():
                    print("Lỗi: Số lượng vé muốn hủy phải là số nguyên dương hợp lệ!")
                    print()
                    continue
                    
                refund_quantity = int(str_refund_qty)
                if refund_quantity <= 0:
                    print("Lỗi: Số lượng vé hủy phải lớn hơn 0.")
                    print()
                    continue
                    
                process_refund(refund_quantity)
                print()
                
            case "3":
                print()
                print_flight_report()
                print()
                
            case "4":
                print("\nĐóng hệ thống! Phiên làm việc kết thúc.")
                break
                
            case _:
                print("Lỗi: Chức năng không hợp lệ! Vui lòng chọn từ 1 đến 4.\n")

if __name__ == "__main__":
    main()