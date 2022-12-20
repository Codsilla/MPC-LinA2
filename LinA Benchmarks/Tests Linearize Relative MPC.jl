using LinA, Dates, BenchmarkTools

include("naiveLinearize.jl")

time = string(today())





relFunc=
    [:(0.0000002*x^5-0.0000274*x^4+0.00151450*x^3-0.02453270*x^2+ 1.92434870*x+ 5.90568630)
    ,:(0.001*x^3-0.024*x^2+ 1.92*x+ 5.91)
    ,:(-0.005*x^3+ 0.5*x^2-0.8*x+ 10.0)
];

println("------Heuristic------")
#Relative Errors
io = open("ResultsRelativeHeuristic "*time*".txt", "w+");
#io=stdout

for f in relFunc
    println(f)
    println(io,f)
    global i = f 
    for bounding ∈ [Under(), Over(), Best()]
            println(io,typeof(bounding))
        for ε ∈ [1,0.1,0.01]
            temp = Linearize(i,1.0,60.0,Relative(ε), bounding=bounding)
            t = @belapsed Linearize(i,1.0,60.0,Relative($ε), bounding=$bounding,)
            println(io,"tolerence : ", ε, " %,  pieces  ", length(temp), ", time : ", t, "  sec")
            flush(io)
        end
    end
end
close(io)



println("------Exact------")

io = open("ResultsRelativeExact "*time*".txt", "w+");
#io=stdout

for f in relFunc
    println(f)
    println(io,f)
    global i = f 
    for bounding ∈ [Under(), Over(), Best()]
            println(io,typeof(bounding))
        for ε ∈ [1,0.1,0.01]
            temp = Linearize(i,1.0,60.0,Relative(ε),ExactLin(), bounding=bounding)
            t = @belapsed Linearize(i,1.0,60.0,Relative($ε), bounding=$bounding,)
            println(io,"tolerence : ", ε, " %,  pieces  ", length(temp), ", time : ", t, "  sec")
            flush(io)
        end
    end
end
close(io)


println("------Naive------")

io = open("ResultsRelativeNaive "*time*".txt", "w+");
#io=stdout


nativeRelFunc = 
[x-> 0.0000002*x^5-0.0000274*x^4+0.00151450*x^3-0.02453270*x^2+ 1.92434870*x+ 5.90568630
,x-> 0.001*x^3-0.024*x^2+ 1.92*x+ 5.91
,x-> -0.005*x^3+ 0.5*x^2-0.8*x+ 10.0
];


for f in 1:length(nativeRelFunc)
    println(relFunc[f])
    println(io,relFunc[f])
    global i = nativeRelFunc[f] 
    for ε ∈ [1,0.1,0.01]
        temp = interpolator_bounded_error(i,1.0,60.0,Relative(ε))
        println(io,"tolerence : ", ε, " %,  pieces  ", length(temp))
        flush(io)
    end
end
close(io)