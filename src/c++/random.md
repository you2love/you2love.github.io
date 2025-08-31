# random
<!-- toc --> 

## 利用费根鲍姆迭代模型产生随机数

```c++
#include <iostream>
#include <fstream>
using namespace std;
int main(int argc, char* argv[])
{
    ofstream of("rand.txt");
    double init_seed = 0.990976548;
    double last = init_seed;
    for (int i=0; i<1000; i++)
    {
        last = 4*last*(1-last);//Xn+1 = CXn(1-Xn)其中c=4
        of<<last<<endl;
    }
    cout<<"create over"<<endl;
    of.close();
    return 0;
}
```
