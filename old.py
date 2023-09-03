
def main():

    raw_numbers = [7.96, 8.95, 8.92, 8.11, 8.06, 8.59, 0, 8.61, 8.88, 8.59]
    numbers = [x - 0.5 for x in raw_numbers]

    big = []
    small = []
    temp = []
    compensate: bool = False

    minimum = round(8.0 * 0.8, 2) # 6.4
    print(f"Minimum: {minimum}")
    for num in numbers:
        big_n = round(num * 0.8, 2)
        small_n = round(num * 0.2, 2)
        missing_time = 0.0
        if compensate and big_n < minimum:
            missing_time = round(minimum - big_n, 2)

            while True:
                if big_n >= minimum or small_n <= 0.0:
                    small_n = round(small_n, 2)
                    big_n = round(big_n, 2)
                    break 

                small_n = small_n - 0.01
                
                big_n = big_n + 0.01      


        #temp.append(missing_time)
        big.append(big_n)
        small.append(small_n)


    print(f"small: {small}")
    print(f"big: {big}")
    #print(temp)

if __name__ == "__main__":
    main()