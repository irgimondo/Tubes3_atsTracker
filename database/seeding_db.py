import os
import logging
import mysql.connector
from mysql.connector import Error
from faker import Faker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("cv_seeding.log", mode='w', encoding="utf-8"),
        logging.StreamHandler()
    ]
)

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'ats_db'
}

DATA_DIR = "data"
fake = Faker('id_ID')


def get_dataset_files(data_folder_path: str) -> list:
    """
    Mengambil 20 file CV pertama dari setiap folder.
    """
    all_selected_files = []
    try:
        categories = sorted([d for d in os.listdir(data_folder_path) if os.path.isdir(os.path.join(data_folder_path, d))])
    except FileNotFoundError:
        logging.error(f"Folder data tidak ditemukan: {data_folder_path}")
        return []

    for category in categories:
        category_path = os.path.join(data_folder_path, category)
        try:
            files_in_category = sorted([f for f in os.listdir(category_path) if f.lower().endswith('.pdf')])
            selected_files = files_in_category[:20]
            for file_name in selected_files:
                full_path = os.path.join(category_path, file_name)
                all_selected_files.append(os.path.normpath(full_path))
        except Exception as e:
            logging.warning(f"Gagal membaca folder '{category}': {e}")
            continue
    return all_selected_files


def main():
    """
    Fungsi utama untuk menjalankan alur seeding.
    Menggunakan metode TRUNCATE untuk mereset database.
    """
    logging.info("Memulai proses seeding.")
    cv_files = get_dataset_files(DATA_DIR)
    if not cv_files:
        return
    logging.info(f"Ditemukan {len(cv_files)} file untuk diproses.")

    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        logging.info("Koneksi database berhasil.")

        for cv_path in cv_files:
            filename = os.path.basename(cv_path)
            logging.info(f"Memproses: {filename}")

            full_name = fake.name()
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ''
            phone = fake.phone_number()
            address = fake.address()
            birth_date_obj = fake.date_of_birth(minimum_age=22, maximum_age=55)
            birth_date_str = birth_date_obj.strftime('%Y-%m-%d')

            try:
                sql_profile = """
                    INSERT INTO ApplicantProfile
                    (first_name, last_name, phone_number, address, date_of_birth)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_profile, (
                    first_name, last_name, phone, address, birth_date_str
                ))
                applicant_id = cursor.lastrowid

                category = os.path.basename(os.path.dirname(cv_path))
                sql_detail = "INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path) VALUES (%s, %s, %s)"
                cursor.execute(sql_detail, (applicant_id, category, cv_path))

                logging.info(f"Data untuk '{full_name}' (ID: {applicant_id}) disimpan.")

            except Error as e:
                logging.error(f"Gagal menyimpan {filename}: {e}")
                conn.rollback()

        conn.commit()
        logging.info("Proses seeding selesai.")

    except Error as e:
        if e.errno == 1045:
            logging.error(f"Koneksi Gagal: Akses ditolak untuk user '{DB_CONFIG['user']}'.")
        elif e.errno == 1049:
            logging.error(f"Database '{DB_CONFIG['database']}' tidak ditemukan.")
        else:
            logging.error(f"Kesalahan database: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            logging.info("Koneksi database ditutup.")


if __name__ == "__main__":
    main()
