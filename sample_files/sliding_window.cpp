#include <bits/stdc++.h>
using namespace std;

int przedzial(vector<int> &v, int r) // searching for such c, so that in the interval [c - r, c + r] there are the most numbers from the vector v
{
    sort(v.begin(), v.end());
    int i = 0;
    int j = 0;
    int s = v.size();
    int ile_wyn = 0; // how many numbers can fit int the interval "height" 2 * r
    int wyn = 0;     // the middle of the interval
    while (j < s)
    {
        if (v[j] - v[i] <= 2 * r)
        {
            if (j - i >= ile_wyn)
            {
                ile_wyn = j - i;
                wyn = (v[i] + v[j]) / 2;
            }
            j++;
        }
        else
        {
            i++;
        }
    }
    return wyn;
}
int main()
{
    int n, r;
    cin >> n >> r;
    vector<int> v(n);
    for (int &el : v)
    {
        cin >> el;
    }
    cout << przedzial(v, r);
}