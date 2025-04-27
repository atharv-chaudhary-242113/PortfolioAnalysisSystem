import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import traceback
import tkinter as tk  # Import tkinter (if not already imported)
from tkinter import messagebox  # Import messagebox (if not already imported)


class DBHandler:
    def __init__(self, config, root=None):  # Add root parameter
        """
        Initialize with database configuration
        Args:
            config: Dictionary with host, user, password, database
            root: Tkinter root window (optional, for GUI error messages)
        """
        self.config = config
        self.table_map = {
            'S&P 500 (Top 30)': 'sp500_assets',
            'NASDAQ 100 (Top 30)': 'nasdaq100_assets',
            'Nifty 50 (India)': 'nifty50_assets',
            'Global Blue Chips': 'global_bluechips',
            'Custom': 'custom_portfolios'
        }
        self.root = root  # Store the root window

    def _create_connection(self):
        """Create database connection"""
        try:
            print("Connecting to database with:")
            print(f"  host: {self.config['host']}")
            print(f"  user: {self.config['user']}")
            print(f"  database: {self.config['database']}")
            conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            print("✅ Database connection successful!")
            return conn
        except Error as e:
            error_message = f"Database connection error: {e} " \
                            f"(host={self.config['host']}, user={self.config['user']}, " \
                            f"database={self.config['database']})"
            print(error_message)
            if self.root:
                messagebox.showerror("Database Error", error_message)
            return None

    def initialize_tables(self):
        """Create all required tables if they don't exist"""
        conn = None
        try:
            conn = self._create_connection()
            if conn is None:
                return False

            cursor = conn.cursor()

            for table_name in self.table_map.values():
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ticker VARCHAR(20) NOT NULL,
                        date DATE NOT NULL,
                        price DECIMAL(15,2) NOT NULL,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE KEY (ticker, date)
                    """)
                print(f"Created table {table_name} if not exists")

            conn.commit()
            return True

        except Error as e:
            error_message = f"Database error during table initialization: {e}\n{traceback.format_exc()}"
            print(error_message)
            if self.root:
                messagebox.showerror("Database Error", error_message)
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()

    def upload_data(self, df, group_name):
        """
        Upload DataFrame to appropriate table
        Args:
            df: DataFrame with Ticker, Date, Price
            group_name: Name of the ticker group
        Returns:
            bool: True if successful
        """
        conn = None
        try:
            table_name = self.table_map.get(group_name, 'custom_portfolios')
            conn = self._create_connection()
            if conn is None:
                return False

            cursor = conn.cursor()

            # Insert data with batch processing
            data = [(row['Ticker'], row['Date'], row['Price'])
                    for _, row in df.iterrows()]

            stmt = f"""
                INSERT INTO {table_name} (ticker, date, price)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE price = VALUES(price)
            """

            print(f"SQL Query: {stmt}")  # Print the SQL query
            print("First few rows of data to be inserted:")
            print(df.head())  # Print first few rows of data

            cursor.executemany(stmt, data)
            conn.commit()

            print(f"✅ Uploaded {len(data)} records to {table_name}")
            return True

        except Error as e:
            error_message = f"Error uploading to {table_name}: {e}\n{traceback.format_exc()}"
            print(error_message)
            if self.root:
                messagebox.showerror("Database Error", error_message)
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()