#include <math.h>
#include <stdlib.h>

// Function to calculate new angle
double calculate_new_angle(double current_angle, double angle_step) {
    return current_angle + angle_step;
}

// Function to calculate wedge positions (x1, y1, x2, y2) based on angle
void calculate_wedge_positions(double wheel_radius, double center_x, double center_y, double angle, double angle_step, double* positions) {
    double x1 = center_x + wheel_radius * cos(angle);
    double y1 = center_y + wheel_radius * sin(angle);
    double x2 = center_x + wheel_radius * cos(angle + angle_step);
    double y2 = center_y + wheel_radius * sin(angle + angle_step);

    positions[0] = x1;
    positions[1] = y1;
    positions[2] = x2;
    positions[3] = y2;
}

// Function to slow down the rotation speed
double slow_down(double speed, double factor) {
    return speed * factor;
}

// Function to generate a random color (optional)
int generate_random_color() {
    return rand() % 0xFFFFFF;
}