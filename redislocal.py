import redis
import rest
def set_redis_value(key, value, host='localhost', port=6379, db=0, password=None):
    """
    Set a value in Redis.

    Parameters:
        key (str): The key to set in Redis.
        value (str): The value to set for the key.
        host (str): Redis server host. Default is 'localhost'.
        port (int): Redis server port. Default is 6379.
        db (int): Redis database index. Default is 0.
        password (str): Redis server password. Default is None.
    """
    try:
        # Create a Redis connection pool
        redis_pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)

        # Create a Redis client
        redis_client = redis.Redis(connection_pool=redis_pool)

        if (redis_client.exists(key)):

            val = redis_client.get(key)

            if (val.decode('utf-8') != value):
                redis_client.set(key, value)
                print("Redis ", val)
                print("Set value ", value)
                print("ok ", val.decode('utf-8') != value)

                form_data = {
                    'message': value,
                    # Add more parameters as needed
                }
                response = rest.call_api_with_post_form_data('http://localhost:5001/publish', form_data)

                if response is not None:
                    print("API call successful!")
                    print("Response:")
                    print(response.text)
                else:
                    print("API call failed.")

        else:
            redis_client.set(key, "on")


        # print(f"Set key '{key}' with value '{value}' in Redis.")
    except Exception as e:
        print(f"Error setting value in Redis: {e}")

# Example usage:
set_redis_value('example_key', 'example_value')



# Example usage:
url = 'http://example.com/api'




