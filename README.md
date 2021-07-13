# kdtreebenchmark
Benchmarking k-d tree construction and search 

Construction of k-d trees is usually performed by pre-sorting the elements and then constructing the tree. This leads to a balanced tree and provides the O(log(n)) time for search. In practice elements to be inserted into a tree are not always fully known at creation, or may be so large that sorting is time consuming in itself. Even when they are known, the performance of a tree may degrade over time with repeated inserts. This level of degradation in performance is the point of interest.

## Dependencies

- python 3.9.5
- kdtree 0.16
>pip install kdtree

## Files

File  | Description
------------- | -------------
benchmark.py | python script to time creation and search of 3d and 4d k-d tree
kdtreebenchmark.ipynb | jupyter notebook of same
pantones.py | python file containing two arrays - pantone name and rgb equivalent
results.ods  | Benchmark timings for pre/random/seeded construction and search
stats.ods  | Simple comparison of values (%,stddev,avg)


### Inspired by

- [pantone to rgb converter](https://codebeautify.org/pantone-to-rgb-converter)
- [Using k-d trees to efficiently calculate nearest neighbors in 3D vector space](https://blog.krum.io/k-d-trees/)
- [How to Search Data with KDTree](https://towardsdatascience.com/how-to-search-data-with-kdtree-aad5c82ebd99)


## Conclusions

The initial expectation of a pre-sorted tree performing better than a random or seeded tree holds. Though at lower volumes of elements the performance was negligible, the small volume and small dimensionality of the datasets did not drastically impact the performance of the tree being less balanced. Computing power was simply the overwhelming factor determining performance in those cases.

Perhaps the most pressing take away was the small difference in the trees’ search performance. Whilst 2-4% is not negligible it is also not exceptional.

There are two key scenarios:
- First that this level of difference in search performance holds when extrapolated to higher orders of magnitude number of elements
- Secondly that this level of difference only worsens with increasing numbers of elements.

In both these cases there is a threshold at which sorting the inputs costs less than the lost time to decreased search performance. Given the large difference in construction times, this seems the best option given a wholly known dataset as the increased sort time is offset by the decreased construction time before the first search is even performed.

The other point of interest is that the construction of a kd-tree over time through random insertion (or pre-seeding) does not lead to drastically worse performance. At least, not in lower order dimensions. Hence the need to re-balance or re-build a kd-tree is not necessary if the performance of search upon its elements can bear an approximate 5% reduction in performance.

