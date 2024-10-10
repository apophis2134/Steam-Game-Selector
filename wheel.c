#include <math.h>
#include <stdlib.h>

#define M_PI 3.14159265358979323846

void calculate_wedge_positions(double radius, double centerX, double centerY, double angle, double angle_step, double* positions) {
    positions[0] = centerX + radius * cos(angle);
    positions[1] = centerY + radius * sin(angle);
    positions[2] = centerX + radius * cos(angle + angle_step);
    positions[3] = centerY + radius * sin(angle + angle_step);
}

unsigned int generate_random_color() {
    unsigned int color = 0;
    for (int i = 0; i < 3; i++) {
        color = color << 8;
        color += rand() % 256;
    }
    return color;
}

double calculate_new_angle(double current_angle, double angle_step) {
    return current_angle + angle_step;
}

double slow_down(double speed, double factor) {
    return speed * factor;
}