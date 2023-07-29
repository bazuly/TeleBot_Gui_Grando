import asyncpg
import Grando_pro.config as config


# db connection
async def insert_data_into_db(car_number, driver_name, date_start, date_end,
                              trans_name, screenshot):
    try:
        print(config.DB_NAME)
        db_connection = await asyncpg.connect(host=config.DB_HOST,
                                              port=config.DB_PORT,
                                              database=config.DB_NAME,
                                              user=config.DB_USER,
                                              password=config.DB_PASS)

        # db creation if needed
        await db_connection.execute("""
                CREATE TABLE IF NOT EXISTS Grando_FTL_screen_test (
                    id SERIAL PRIMARY KEY,
                    car_number VARCHAR(255) NOT NULL,
                    driver_name VARCHAR(255) NOT NULL,
                    date_start DATE NOT NULL,
                    date_end DATE NOT NULL,
                    trans_name VARCHAR(255),
                    screenshot text

                )
            """)

        await db_connection.execute(
            'INSERT INTO Grando_FTL_screen_test (car_number, driver_name, date_start, date_end, trans_name, screenshot)'
            'VALUES ($1, $2, $3, $4, $5, $6)', car_number, driver_name,
            date_start, date_end, trans_name, screenshot)
        await db_connection.close()
        print('Data inserted')
    except asyncpg.PostgresError as e:
        print('Error:', e)


