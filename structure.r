library(bnlearn)

matpor <- read.csv("C:/python/bn/matpor.csv")[,-1]


a1 <- pc.stable(matpor, alpha=0.01)
a2 <- pc.stable(matpor, alpha=0.05)
a3 <- pc.stable(matpor, alpha=0.99)
a4 <- pc.stable(matpor, alpha=0.15)

plot(a1)

matpor$age <- cut(matpor$age, c(0,5,10,15,20,25))
matpor$G1 <- cut(matpor$G1, c(-1,5,10,15,20,25,30,35))
matpor$G2 <- cut(matpor$G2, c(-1,5,10,15,20,25,30,35))
matpor$G3 <- cut(matpor$G3, c(-1,5,10,15,20,25,30,35))


matpor[] <- lapply(matpor, as.factor)

d.discrete <- apply(matpor, 2,
  function(x,N=5)
    cut(x,quantile(x,probs=seq(0,1,length.out=N)),
        include.lowest = TRUE)
)
