

# Usage of the LinA package

All the useful documentation should be accessible through the `?` native Julia command to access documentation. (ex. do ?Linearize() to access the documentation of that function)
## Usage Example
If we want to Linearize $f(x) = x^2$ from -10 to 10 with a maximum absolute error of $2$ simply do
```julia
julia> using LinA

julia> pwl = Linearize(:(x^2),-10,10,Absolute(2))
5-element Vector{LinA.LinearPiece}:
 -16.000000000000004 x -62.00000000000003 from -10.0 to -6.0
 -8.0 x -14.0 from -6.0 to -2.0
 0.0 x + 2.0 from -2.0 to 2.0
 8.0 x -14.0 from 2.0 to 5.999999999999999
 15.999999999999996 x -61.99999999999998 from 5.999999999999999 to 10.0

```
**Note:** by default LinA uses the hybrid heuristic algorithm. To use the exact algorithm simply add `ExactLin()` as an argument.

You can now call `pwl` as a julia function such as

```julia
julia> pwl(2)
4.470129472588532
```
But also as an array to get the individual linear segments such as
```julia 
julia> pwl[2]
-8.0 x -14.0 from -6.0 to -2.0

julia> pwl[2].xMax
-2.0
```
## Plotting
Pwl functions are compatible with Plots.jl. To plot a pwl function simply do
```julia
using Plots

plot(x->pwl(x),-10,10)

```
![alt text](https://i.imgur.com/7IHj3qp.png)


# Benchmarks
Two different sets of benchmarks are available. The first one is to directly asses the efficiency of LinA and the second one to reproduce the results on the network design problem.

## LinA Benchmarks
Running `Tests Linearize Absolute MPC.jl` and `Tests Linearize Relative MPC.jl` will run benchmarks on every function mentioned in the paper using BenchmarkTools.jl. The results are outputted in log files in the same directory.

## Network Design Benchmarks
Since there are hundreds of instances many reaching the time limit of 3600 seconds we did not include a script to run every instance at once. However, instances can be tested individually. To do so, simply do

```julia
include("model_CMCND_Nodes_Graph.jl")
graphModelCongestion(instance, InstanceVersion, IncremCosts) 
```
**Explanation:** Each instance has 6 variations (in the original paper, they created variations of each instance to have a bigger set of instances). We have that $InstanceVersion \in \{"03","08"\}$ and $IncremCosts \in \{:IncremCosts6,:IncremCosts7,:IncremCosts8 \}$

For example,
```julia
graphModelCongestion("c33", "03", :IncremCosts8) 
```
Will run the instance c33 version 03 with incremCost 8. In the paper, the results for time and gap are averaged over the 6 versions.

By default the time limit for CPLEX is 3600 seconds. This can be changed simply with the keyword arguments `timeLmit`
```julia
graphModelCongestion("c33", "03", :IncremCosts8,timeLimit=20) 
```
For the full list of instance and for more details see the documentation of `graphModelCongestion`

**Note:** In addition to the CPLEX output, this function also creates a log files with some statistics about the solution found. (In the Results folder)
