

using CSV, MetaGraphs, CPLEX, JuMP , Graphs# LightGraphs,
using LinA, DataFrames, Roots, LinearAlgebra
include("naiveLinearize.jl")



"""
The instance are "c33", "c35", "c36", "c37", "c38", "c39", "c40", "c41", "c42", "c43", "c44", "c45", "c46", "c47", "c48", "c49", "c50", "c51", "c52", "c53", "c54", "c55", "c56", "c57", "c58", "c59", "c60", "c61", "c62", "c63", "c64", "c25_100_10_F_L_5","c25_100_10_F_T_5","c25_100_10_V_L_5","c25_100_30_F_L_5", "c25_100_30_F_T_5","c25_100_30_V_T_5","c100_400_10_F_L_10", "c100_400_10_F_T_10", "c100_400_10_V_L_10", "c100_400_30_F_L_10", "c100_400_30_V_T_10"

InstanceVersion is either "03" or "08"

IncremCost is either :IncremCosts6, :IncremCosts7 or :IncremCosts8

naiveLin is a boolean that sets the type of linearization used

precision sets the relative precision of the linearization
"""
function CMCND_cplex_pwl(instance,InstanceVersion,IncremCosts;naiveLin = false, precision =1)

    #Constant given in the original paper
    F=1
    α=3
    β=1;

    folder = ""

    if naiveLin
        folder = "naive"
    else
        folder = "lina" 
    end

    stdstdout = stdout

    infoGraph=CSV.read("formatedData/$(instance).csv",DataFrame; copycols=true)
    sort!(infoGraph)
    
    commodity=CSV.read("formatedData/$(instance)Commod.csv",DataFrame)
    infoNode=CSV.read("formatedData/infoNodes/nodes_$(instance)_$(InstanceVersion).csv",DataFrame);

    bpxLogs = open("pwlData/"*folder*"/$(instance)_$(InstanceVersion)_$(String(IncremCosts)[end])"*".bpx","w")
    bpValLogs = open("pwlData/"*folder*"/$(instance)_$(InstanceVersion)_$(String(IncremCosts)[end])"*".bpval","w")

    println(bpxLogs,"#node,#breakpoints")
  



    #initialization of the graph
    nbNode = maximum([maximum(infoGraph[!,:from]),maximum(infoGraph[!,:to])])
   
   

    G = DiGraph(nbNode)


    add_edge!.((G,), infoGraph[!,:from], infoGraph[!,:to])



    mg = MetaDiGraph(G);

    i=0;


    
    for v in vertices(mg)


        D = infoNode[v,:D]
        capacity = infoNode[v,:InitCapacity]
        capaMax = capacity + infoNode[v,:IncremCapacity]

        
        #Congestion function with the initial cost
        g_expr= :($D* ($F *x + $β* x^(1+$(α))/$(capacity)^$(α)))
        g = x ->   D* ( F* x +  β* x^(1+  α)/  (capacity)^  α)

        #Congestion function with the upgraded cost (initial value = upgradeCost)
        gu_expr = :($( infoNode[v,IncremCosts]) + $D* ($F*x+$β*(x^(1+$α)/$(capaMax)^$α)))
        gu = x ->  infoNode[v,IncremCosts] + D*(F*x+β*(x^(1+α)/capaMax^α))

        if gu(capacity) < g(capacity)
            croisement = find_zero(x->(g(x)-gu(x)),(0,capacity))
        else
            croisement = capacity
        end


        #Linearization of the congestion function
        if naiveLin
            pwlNotUpgraded = interpolator_bounded_error(g,0, croisement ,Relative(precision), bounding = Over())
            pwlUpgraded = interpolator_bounded_error(gu,croisement,capaMax,Relative(precision),bounding = Over())
        else

            pwlNotUpgraded = Linearize(g, 0, croisement, Relative(precision); bounding = Over())
            pwlUpgraded = Linearize(gu,croisement,capaMax,Relative(precision),bounding = Over())
        end


        pwl = [pwlNotUpgraded;pwlUpgraded]
        #println.(pwl)CpleXBreakpoints(pwl)
        temp = CplexBreakpoints(pwl)
        temp2 = round.(pwl.(temp),digits=5)
        temp = round.(temp,digits=5)
        
        println(bpxLogs,v,",",length(temp),",",join(temp,","))
        println(bpValLogs,v,",",length(temp2),",",join(temp2,","))

        

    end
    close(bpxLogs)
    close(bpValLogs)

end
