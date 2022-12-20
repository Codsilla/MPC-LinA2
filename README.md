

# Usage of the LinA package

All the useful documentation should be accessible through the `?` native Julia command to access documentation. (ex. do ?Linearize() to access the documentation of that function). The full documentation can be found at https://lico-labs.github.io/LinA.jl/.

## Usage Example
To Linearize $f(x) = x^2$ from -10 to 10 with a maximum absolute error of $2$ simply do
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
`Linearize` also works with native Julia functions
```julia
julia> using LinA

julia> Linearize(x->x^3+10,-2,2,Relative(5))
5-element Vector{LinA.LinearPiece}:
 9.299132471956174 x + 20.698254943912346 from -2.0 to -1.4199827767895903
 2.5362123473279845 x + 11.095024846136608 from -1.4199827767895903 to -0.2403648690183138
 -4.099594510183635 x + 9.50001 from -0.2403648690183138 to 0.0
 1.9208943589791683 x + 9.49999 from 0.0 to 1.4219683759083164
 11.443392082478248 x -4.040700622474624 from 1.4219683759083164 to 2.0

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
Since there are hundreds of instances in which many reached the time limit of 3600 seconds in our benchmarks, we did not include a script to run every instance at once. To test our numerical results, you can run any instance located in `pre-generated LPs\LinA` and `pre-generated LPs\naive`.

For example, while in the right folder, simply start CPLEX and type
```
set Threads 1
set timelimit 3600
read "naive/LPs/c100_400_10_F_L_10_03_6.lp"
opt
```


To also test the LPs generation, you will need to go through a 2 steps process
- Create the plws functions for your instance
- Create the LP using those plws

  
The reason for this separation is that Julia doesn't have a way to give plw functions to CPLEX in a native way. Since we wanted to use CPLEX great implementation of plw functions (way faster than simply giving a binary variable per segment), we had to resort to creating the plws in Julia, saving them in a file, and then creating the model in python.  


To generate the plws for a given instance, start Julia and type: 

```julia
include("generate pwl CMCND.jl")
CMCND_cplex_pwl(instance, InstanceVersion, IncremCosts;naiveLin, precision) 
```
**Explanation:** Each instance has 6 variations (in the original paper, they created variations of each instance to have a bigger set of instances). We have that $InstanceVersion \in \{$"$03$","$08$"$\}$ and $IncremCosts \in \{:IncremCosts6,:IncremCosts7,:IncremCosts8 \}$

For example,
```julia
CMCND_cplex_pwl("c33", "03", :IncremCosts8;naiveLin=true, precision=2 ) 
```
Will create the PWLs for the instance c33 version 03 with incremCost 8 with the naive algorithm with a precision of $2\%$. The resulting PWLs will be stored in the folder pwlData.

For the full list of instances and for more details see the documentation of `CMCND_cplex_pwl`

To then create the linear program, you will need to call `MCNDbuildmodelgenerateLPfile.py`. For example,

```
python3 MCNDbuildmodelgenerateLPfile.py c33 03 6 Lina
```


