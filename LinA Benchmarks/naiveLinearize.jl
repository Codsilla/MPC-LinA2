using LinA, Roots

sampler(f,n,a,b) = [(x,f.(x)) for x in a:(b-a)/(n-1):b+1e-7]

function joint2Dots(p1,p2) 

    a = (p2[2]-p1[2])/(p2[1]-p1[1])
    b = p1[2]- a*p1[1]
    
    LinA.LinearPiece(p1[1], p2[1], a, b, x->a*x+b)

end

function naiveNpoints(f,n,a,b)
    
    dots = sampler(f,n,a,b)
    
    [joint2Dots(dots[i],dots[i+1]) for i in 1:n-1]
end

function interpolator_bounded_error(f,x1,x2,e::LinA.ErrorType;bounding::LinA.BoundingType = LinA.Best())
    epsilon = 1e-5
    
    (x1,x2,lower,upper,_) = LinA.CorridorFromInfo(x1,x2,f,e,bounding)
    n = 1
    
    while true
        n+=1
        pwl = naiveNpoints(f,n,x1,x2)
        t = pwl[end]
        pwl[end] = LinA.LinearPiece(t.xMin, x2, t.a, t.b, t.fct)

        errorLower(x) = pwl(x) - lower(x) + epsilon
        find_zeros(errorLower,x1,x2) != [] && continue
        errorUpper(x) = upper(x) - pwl(x) + epsilon
        find_zeros(errorUpper,x1,x2) != [] && continue
        
        return pwl
        
    end
end
