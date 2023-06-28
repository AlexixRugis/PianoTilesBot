#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    int n, m, x, y;
    cin >> n >> m >> x >> y;
    vector<int> w_weights(m, 0);
    vector<int> b_weights(m, 0);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            char c;
            cin >> c;
            if (c == '#') {
                w_weights[j]++;
            }
            else {
                b_weights[j]++;
            }
        }
    }

    y = min(y, m);
    x = min(x, y);
    vector<int> w_buffer(y, INT_MAX);
    vector<int> b_buffer(y, INT_MAX);

    w_buffer[0] = w_weights[0];
    b_buffer[0] = b_weights[0];

    int last_w_min = w_buffer[0];
    int last_b_min = b_buffer[0];
    int max_index = min(1, y - 1);
    for (int i = 1; i < m; i++) {
        for (int j = 1; j <= max_index; j++) {
            w_buffer[j] = w_buffer[j - 1] + w_weights[i];
            b_buffer[j] = b_buffer[j - 1] + b_weights[i];
        }

        w_buffer[0] = last_b_min + w_weights[i];
        b_buffer[0] = last_w_min + b_weights[i];

        last_w_min = INT_MAX;
        last_b_min = INT_MAX;
        for (int j = x - 1; j < y; j++) {
            last_w_min = min(last_w_min, w_buffer[j]);
            last_b_min = min(last_b_min, b_buffer[j]);
            last_w_min = min(last_w_min, w_buffer[0]);
            last_b_min = min(last_b_min, b_buffer[0]);
        }

        max_index = min(max_index + 1, y - 1);
    }


    int min_v = INT_MAX;
    for (int i = x - 1; i < y; i++) min_v = min(min_v, w_buffer[i]);
    for (int i = x - 1; i < y; i++) min_v = min(min_v, b_buffer[i]);
    cout << min_v;

}
