import os
import psycopg2

""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""


async def is_in_command_count(user_id: int, command_name: str) -> bool:
    """
    This function will check if a user already played a command.

    """
        
    with psycopg2.connect(
        host='wcb3_postgres', dbname='pg_wcb3', user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM command_stats WHERE user_id=%s AND command=%s", (str(user_id), command_name,)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, zeggen we dat command al bestaat
        except:
            return True
        

async def increment_or_add_command_count(user_id: int, command_name: str, amount: int):

    alreadyExists = await is_in_command_count(user_id, command_name)

    with psycopg2.connect(
        host='wcb3_postgres', dbname='pg_wcb3', user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE command_stats SET count = count + %s WHERE user_id=%s AND command=%s",
                        (amount, str(user_id), command_name)
                    )   
                else:
                    cursor.execute(
                        "INSERT INTO command_stats(command, user_id, count) VALUES (%s, %s, %s)",
                        (command_name, str(user_id), amount,)
                    )

                cursor.commit()
                return True
                
        except:
            return False
        

async def set_command_count(command_name, user_id, amount):
    alreadyExists = await is_in_command_count(user_id, command_name)

    with psycopg2.connect(
        host='wcb3_postgres', dbname='pg_wcb3', user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE command_stats SET count = %s WHERE user_id=%s  AND command=%s", 
                        ((amount), str(user_id), command_name,)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO command_stats(command, user_id, count) VALUES (%s, %s, %s)",
                        (command_name, str(user_id), amount,)
                    )
                    
                con.commit()
                return True

        except:
            return False
        

async def get_command_count(user_id, command_name) -> list:
    try:
        with psycopg2.connect(
        host='wcb3_postgres', dbname='pg_wcb3', user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT count FROM command_stats WHERE user_id=%s AND command=%s", 
                    (str(user_id), command_name,)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    
