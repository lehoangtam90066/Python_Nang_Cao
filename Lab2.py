import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bệnh Viện ĐA Cấp Lê Hoàng Tam")

        # Database pdAdmin 4
        
        self.db_name = tk.StringVar(value='thuoc')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='Tamle90066@')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='thuocuong')   

        # Tạo cửa sổ giao diện bệnh viện
        self.create_widgets()

    def create_widgets(self):
        # Giao diện kết nối từ Data pgAdmin 4 đến Visual Studio Code
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="Data:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(connection_frame, text="Phần Mềm:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Mật Khẩu:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Địa Chỉ:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="IP:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Kết Nối", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Truy vấn
        query_frame = tk.Frame(self.root)
        query_frame.pack(pady=10)

        tk.Label(query_frame, text="Bảng:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Truy Cập", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        # Nơi hiển thị văn bản dữ liệu
        self.data_display = tk.Text(self.root, height=10, width=80)  # Vị trí điều chỉnh rộng và cao
        self.data_display.pack(pady=10, fill=tk.BOTH, expand=True)  # Vị trí điều chỉnh ngang và dọc

        # Chèn
        insert_frame = tk.Frame(self.root)
        insert_frame.pack(pady=10)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()
        self.column3 = tk.StringVar()

        tk.Label(insert_frame, text="Tên Bệnh Nhân:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Mắc bệnh:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(insert_frame, text="Lên Đơn Thuốc:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column3).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Tìm Kiếm", command=self.search_data).grid(row=3, columnspan=2, pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Thành Công", "Đã kết nối với DATABASE ")
        except Exception as e:
            messagebox.showerror("Rất Tiếc", f"Không kết nối thành công DATABASE vui lòng thử lại: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def search_data(self):
        try:
            # Tìm kiếm theo tên, bệnh và thuốc
            search_query = sql.SQL("SELECT * FROM {} WHERE Ten LIKE %s AND Benh LIKE %s AND Thuoc LIKE %s").format(sql.Identifier(self.table_name.get()))
            
            # Dùng tham số để tránh SQL Injection
            data_to_search = ('%' + self.column1.get() + '%', '%' + self.column2.get() + '%', '%' + self.column3.get() + '%')
            
            self.cur.execute(search_query, data_to_search)
            rows = self.cur.fetchall()

            # Hiển thị kết quả 
            self.data_display.delete(1.0, tk.END)
            if rows:
                for row in rows:
                    self.data_display.insert(tk.END, f"{row}\n")
            else:
                messagebox.showinfo("Kết Quả", "Không tìm thấy kết quả nào.")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã có lỗi trong quá trình tìm kiếm: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
