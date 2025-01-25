import numpy as np

def approximate_pi(num_points=1000000):

    # Generate random x and y coordinates between -1 and 1
    x = np.random.uniform(-1, 1, num_points)
    y = np.random.uniform(-1, 1, num_points)

    # Check if points are inside the unit circle: x^2 + y^2 ≤ 1
    distances_squared = x**2 + y**2
    inside_circle = np.sum(distances_squared <= 1)

    # Calculate pi approximation
    pi_approx = 4 * (inside_circle / num_points)
    return pi_approx

if __name__ == "__main__":
    num_points = int(input("Enter the number of points to generate: "))
    pi_estimate = approximate_pi(num_points=num_points)
    print(f"Approximated value of pi using {num_points} points: {pi_estimate}")