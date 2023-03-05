# 换位法生成全排列

```c++
#include <iostream>
#include <string>
#include <bitset>
#include <fstream>
#include <stdio.h>

const int array_length = 30;

template <typename T>
int get_max_active(const int* ptr_array,
           int length,
           const T& ptr_array_flag)
{
  int max_index = -1;
  for (int i=0; i<length; i++)
    {
      int j;
      if (ptr_array_flag[i])//from left to right
    {
      j = i+1;
      while (j<length)
        {
          if (ptr_array[i] > ptr_array[j++])// has active state data
        {
          if ((max_index == -1) || (ptr_array[max_index] < ptr_array[i]))
            {
              max_index = i;
            }
          break;
        }
        }
    }
      else// from right to left
    {
      j = i-1;
      while (j >= 0)
        {
          if (ptr_array[i] > ptr_array[j--])
        {
          if ((max_index == -1) || (ptr_array[max_index] < ptr_array[i]))
            {
              max_index = i;
            }
          
          break;
        }
        }// end of while
    }// end of if
    }// end of for
  return max_index;
}

template <typename T>
void gen_arrange(int* ptr_array, int length, T& ptr_array_flag)
{
  std::ofstream out_file("arrange.txt");
  int max_index = -1;// -1 is no active data
  int max_data;
  while ( (max_index = get_max_active(ptr_array, length, ptr_array_flag)) != -1)
    {
      for (int k=0; k<length; k++)
    {
      out_file<<ptr_array[k]<<"|";
    }      
                  
      out_file<<std::endl;
      
      max_data = ptr_array[max_index];

      //change heig
      if (ptr_array_flag[max_index])//from left to right
    {
      //change flag
      if (!ptr_array_flag[max_index+1])
        {
          ptr_array_flag.flip(max_index+1);
          ptr_array_flag.flip(max_index);
        }

        //change value      
      ptr_array[max_index]   += ptr_array[max_index+1];
      ptr_array[max_index+1] = ptr_array[max_index] - ptr_array[max_index+1];
      ptr_array[max_index]   -= ptr_array[max_index+1];
    }
      else//from right to left
    {      
      //change flag
      if (ptr_array_flag[max_index+1])
        {
          ptr_array_flag.flip(max_index);
          ptr_array_flag.flip(max_index+1);
        }
      //change value
      ptr_array[max_index]   += ptr_array[max_index-1];
      ptr_array[max_index-1] = ptr_array[max_index] - ptr_array[max_index-1];
      ptr_array[max_index]   -= ptr_array[max_index-1];
    }//end of if

      //change better than max_data flag
      for (int j=0; j<length; j++)
    {
      if (ptr_array[j] > max_data)
        {          
          ptr_array_flag.flip(j);//change flag          
        }
    }
    }//end of while

  for (int k=0; k<length; k++)
    {
      out_file<<ptr_array[k]<<"|";
    }
  out_file<<std::endl;
}


int main(int argc, char* argv[])
{
  int array[array_length];

  //init array data
  for (int i=0; i<array_length; i++)
    {
      array[i] = i+1;
    }

  std::string str_flag;
  //init array flag from right to left
  for (int i=0; i<array_length; i++)
    {
      str_flag +='0';
    }

  std::bitset<array_length> array_flag(str_flag);
  gen_arrange(array, array_length, array_flag);  
  return 0;
}

```
