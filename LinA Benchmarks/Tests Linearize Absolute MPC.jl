using LinA, Dates, BenchmarkTools

include("naiveLinearize.jl")

time = string(today())


# Complicated function from Maranas & Floudas (1994)
#(function AX in our paper)

function computefAX(;fct=false)
    THETA=109.5*pi/180
    costh=cos(THETA)
    CosTh2=costh*costh
    SinTh2=(sin(THETA))^2
    R=1.54 #covalence bond length
    R2=R*R

    C1 = 2 * pi * -1 / 3
    C2 = 0
    C3 = 2 * pi * 1 / 3

    K=3 * R2 - 4 * R2 * costh

    f1(x)=
    (7 +
    588600 / ((K - 2 * R2 * (SinTh2*cos(x+C1)-CosTh2))^6) +
    600800 / ((K - 2 * R2 * (SinTh2*cos(x)-CosTh2))^6) +
    481300 / ((K - 2 * R2 * (SinTh2*cos(x+C3)-CosTh2))^6) -
    1079.1 / ((K - 2 * R2 * (SinTh2*cos(x+C1)-CosTh2))^3) -
    1071.5 / ((K - 2 * R2 * (SinTh2*cos(x)-CosTh2))^3) -
    1064.6 / ((K - 2 * R2 * (SinTh2*cos(x+C3)-CosTh2))^3)
    )
    if fct
        return f1
    end

    expr1 = :( 7 +
    588600 / (($K - 2 * $R2 * ($SinTh2*cos(x+$C1)-$CosTh2))^6) +
    600800 / (($K - 2 * $R2 * ($SinTh2*cos(x)-$CosTh2))^6) +
    481300 / (($K - 2 * $R2 * ($SinTh2*cos(x+$C3)-$CosTh2))^6) -
    1079.1 / (($K - 2 * $R2 * ($SinTh2*cos(x+$C1)-$CosTh2))^3) -
    1071.5 / (($K - 2 * $R2 * ($SinTh2*cos(x)-$CosTh2))^3) -
    1064.6 / (($K - 2 * $R2 * ($SinTh2*cos(x+$C3)-$CosTh2))^3)
    )

    return expr1
end


p = (0.1,0.05,0.01,0.005)
expr = [:(x^2),:(log(x)),:(sin(x)),:(tanh(x)),:(sin(x)/x),:(2x^2+x^3),:(exp(-x)*sin(x)),:(exp(-100.0(x-2.0)^2.0)), 
    :(1.03*exp(-100(x-1.2)^2) + exp(-100*(x-2)^2)),computefAX()]


ranges = [(-3.5,3.5),(1,32),(0,2*pi),(-5,5),(1,12),(-2.5,2.5),(-4,4),(0,3),(0,3),(0,2π)]
ConcavityChange = [[Inf],[Inf],[Inf],[Inf],[Inf],[Inf],[-1.5707963267948966,1.5707963267948966],[1.92929,2.07071],[1.12929, 1.27071,1.92929,2.07071],[Inf]]
;

println("------Heuristic-----")

io = open("resultsAbsoluteHeuristic "*time*".txt", "w+")
#io=stdout
for i in 1:length(expr)
    println(expr[i])
    println(io,expr[i])
    for δ ∈ p
        fct = expr[i]
        from,to = ranges[i]
        cc= ConcavityChange[i]
        temp = Linearize(expr[i],ranges[i]..., Absolute(δ), ConcavityChanges=ConcavityChange[i])
        t = @belapsed Linearize($fct,$from,$to, Absolute($δ), ConcavityChanges=$cc)
        println(io,"tolerence : ± ", δ,",  pieces  ", length(temp), ", time : ", t, "  sec")
        flush(io)
    end
end
close(io)

println("------Exact-----")

io = open("resultsAbsoluteExact "*time*".txt", "w+")
#io=stdout
for i in 1:length(expr)
    println(expr[i])
    println(io,expr[i])
    for δ ∈ p
        fct = expr[i]
        from,to = ranges[i]
        cc= ConcavityChange[i]
        temp = Linearize(expr[i],ranges[i]..., Absolute(δ), ExactLin(),ConcavityChanges=ConcavityChange[i])
        t = @belapsed Linearize($fct,$from,$to, Absolute($δ), ExactLin(),ConcavityChanges=$cc)
        println(io,"tolerence : ± ", δ,",  pieces  ", length(temp))#, ", time : ", t, "  sec")
    end
end
close(io)

io = open("ResultsRelativeNaive "*time*".txt", "w+");
#io=stdout

println("------Naive------")

fcts = [x->x^2,x->log(x),x->sin(x),x->tanh(x),x->sin(x)/x,x->2x^2+x^3,x->exp(-x)*sin(x)
,x-> exp(-100(x-2)^2),  x-> 1.03*exp(-100(x-1.2)^2) + exp(-100*(x-2)^2),computefAX(fct=true)]


for i in 1:length(fcts)
    println(expr[i])
    println(io,expr[i])
    for δ ∈ p
        fct = fcts[i]
        from,to = ranges[i]
        cc= ConcavityChange[i]
        temp = interpolator_bounded_error(fct,ranges[i]...,Absolute(δ))
        println(io,"tolerence : ± ", δ,",  pieces  ", length(temp))
    end
end
close(io)

