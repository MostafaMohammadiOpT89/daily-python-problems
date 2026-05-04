Use a hash map to store numbers seen so far and their indices. As you iterate through `nums`, compute the complement `target - num`. If that complement has already been seen, you have found the two indices and can return them immediately.

This approach runs in linear time, `O(n)`, because each lookup and insert in the hash map is average `O(1)`.

The tests cover:
- a standard example
- another valid pair
- duplicate values
- negative numbers
- zero as the target
- ensuring two distinct indices are returned