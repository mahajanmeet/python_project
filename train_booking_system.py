from datetime import datetime

class Train:
    def __init__(self, train_id, departure_time, destination, seats, station_number):
        self.train_id = train_id
        self.departure_time = datetime.strptime(departure_time, '%H:%M')
        self.destination = destination
        self.seats = seats
        self.booked_seats = [False] * seats
        self.station_number = station_number

    def book_seat(self, seat_number):
        try:
            if 1 <= seat_number <= self.seats:
                if not self.booked_seats[seat_number - 1]:
                    self.booked_seats[seat_number - 1] = True
                    print(f"\033[92mSeat {seat_number} booked successfully on Train {self.train_id}\033[0m")  # Green color
                else:
                    print(f"\033[91mSeat {seat_number} is already booked on Train {self.train_id}\033[0m")  # Red color
            else:
                print(f"\033[91mSeat {seat_number} is not available on Train {self.train_id}\033[0m")  # Red color
        except IndexError:
            print("\033[91mInvalid seat number\033[0m")

    def check_seat_availability(self):
        available_seats = [i + 1 for i, seat in enumerate(self.booked_seats) if not seat]
        return available_seats

def partition(trains, low, high):
    pivot = trains[high].departure_time
    i = low - 1
    for j in range(low, high):
        if trains[j].departure_time <= pivot:
            i += 1
            trains[i], trains[j] = trains[j], trains[i]
    trains[i + 1], trains[high] = trains[high], trains[i + 1]
    return i + 1

def quicksort(trains, low, high):
    if low < high:
        pi = partition(trains, low, high)
        quicksort(trains, low, pi - 1)
        quicksort(trains, pi + 1, high)

def assign_station_numbers(trains):
    prev_departure_time = None
    for train in trains:
        station_number = 1
        if train.departure_time == prev_departure_time:
            station_number += 1
            prev_departure_time = train.departure_time
            train.station_number = station_number
        else:
            prev_departure_time = train.departure_time
            train.station_number = station_number

def display_train_schedule(trains):
    print("\nTrain Schedule:")
    print("Platform Train ID  Departure Time  Destination  Seat Status")
    for train in trains:
        available_seats = train.check_seat_availability()
        seat_status = ""
        for i in range(1, train.seats + 1):
            if i in available_seats:
                seat_status += f"\033[92m{i}\033[0m "  # Green color for available seats
            else:
                seat_status += f"\033[91m{i}\033[0m "  # Red color for booked seats
        print(f"{train.station_number:<8} {train.train_id:<9} {train.departure_time.strftime('%H:%M'):<15} {train.destination:<12} {seat_status}")

def main():
    trains = []

    while True:
        try:
            num_trains = int(input("Enter the number of trains: "))
            if num_trains <= 0:
                raise ValueError
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a positive integer\033[0m")

    for i in range(num_trains):
        while True:
            try:
                train_id = int(input(f"Enter Train ID for Train {i + 1}: "))
                departure_time = input(f"Enter Departure Time for Train {i + 1} (HH:MM): ")
                datetime.strptime(departure_time, '%H:%M')  # Check if input is a valid time format
                destination = input(f"Enter Destination for Train {i + 1}: ")
                seats = int(input(f"Enter Number of Seats for Train {i + 1}: "))
                print()
                if seats <= 0:
                    raise ValueError
                trains.append(Train(train_id, departure_time, destination, seats, 0))  # Initialize platform number as 0
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter valid values\033[0m")
            except KeyboardInterrupt:
                print("\033[91mProgram terminated\033[0m")
                return

    # Sort trains by departure time using quicksort
    quicksort(trains, 0, len(trains) - 1)

    # Assign station numbers to trains
    assign_station_numbers(trains)

    # Display train schedule
    display_train_schedule(trains)

    # program start from here
    while True:
        try:
            train_id = int(input("Enter the train ID to book a seat (0 to exit): "))
            if train_id == 0:
                break
            else:
                train = next((t for t in trains if t.train_id == train_id), None)
                if train:
                    if train.check_seat_availability():
                        seat_number = int(input("Enter the seat number to book: "))
                        train.book_seat(seat_number)
                    else:
                        print("Train is fully booked. Please try another train.")
                else:
                    print("Invalid train ID. Please try again.")
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    # Display updated train schedule after booking
    display_train_schedule(trains)

if __name__ == "__main__":
    main()
