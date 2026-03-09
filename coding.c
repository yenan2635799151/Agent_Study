int search(vector<int>& nums, int target) {
    int n = nums.size();
    int left = 0,right = n-1;
    while(left <= right){
        int mid = (left + right)/ 2;
        if(nums[mid]==target):
            return mid;
        if(nums[mid]<target)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1;
}


 int removeElement(vector<int>& nums, int val) {
    int count = 0;
        for(int i =0;i<nums.size();i++){
            if(nums[i]==val){
                for(int j=i+1;j<nums.size()-count;j++){
                    nums[j-1] = nums[j];
                }
                count++;
                i--;
        }

    }
     return nums.size()-count;
 }