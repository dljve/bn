# This dataset is a simplified, pre-processed version of the 
# "Adult Income Dataset" from the UCI machine learning repository.
# Download the dataset from Brightspace and save it in your working
# directory, if you haven't already.
#mat <- read.csv("C:/python/bn/student-mat.csv", sep=';')
d <- read.csv("C:/python/bn/student-por.csv", sep=';')
#mat["subject"] <- "mat"
#por["subject"] <- "por"
#d <- rbind(mat, por)
d$G1 <- NULL
d$G2 <- NULL


library(Hmisc)
quantiles <- quantile(d$age, prob = seq(0, 1, length = 11), type = 5)
d$age <- cut(df$age , breaks = quantile(df$vec, c(0, .1,.., 1)), 
              labels=1:10, include.lowest=TRUE)

d$age <- cut2(d$age, g = 4, oneval=FALSE)
d$absences <- cut2(d$absences, g = 4, oneval=FALSE)
d$G3 <- cut2(d$G3, g = 4, oneval=FALSE)


# Let's take a quick look at the levels and distributions of each variable.
for( i in colnames(d) ){
	print(i)
	print(table(d[,i]))
}

# Let us now define a simple DAG for these variables. 
# Use the below command to install the latest version of the dagitty
# R package, if you haven't already. It is important to get the latest
# version, otherwise the testing will not work with categorical data!
#
# devtools::install_github("jtextor/dagitty/r")


library( dagitty )
g <- dagitty('
dag {
absences -> failures
absences -> G3
activities -> freetime
age -> activities
age -> romantic
age -> studytime
failures -> G3
failures -> paid
failures -> schoolsup
failures -> studytime
famrel -> famsup
famrel -> paid
famsup -> G3
famsup -> paid
famsup -> studytime
Fedu -> Fjob
Fedu -> higher
Fjob -> famrel
freetime -> G3
freetime -> studytime
goout -> freetime
goout -> romantic
health -> absences
health -> G3
health -> studytime
higher -> famsup
higher -> school
higher -> studytime
Medu -> higher
Medu -> Mjob
Mjob -> famrel
paid -> freetime
paid -> G3
paid -> studytime
romantic -> freetime
school -> schoolsup
school -> traveltime
schoolsup -> freetime
schoolsup -> G3
schoolsup -> studytime
studytime -> G3
traveltime -> absences
traveltime -> freetime
}
')

# Print out all d-separation statements implied by the DAG.
impliedConditionalIndependencies(g)

sink()# Manually test the implication: HoursPerWeek _||_ Race | Immigrant
chisq <- 0; df <- 0
for( a in unique( d$Immigrant ) ){
	tst <- chisq.test( d$absences[d$traveltime==a], d$G3[d$traveltime==a] )
	chisq <- chisq + tst$statistic
	df <- df + tst$parameter
}
cat( chisq, df, "\n" )
pchisq( chisq, df, lower.tail=FALSE )

# This single command performs a chi-square test for all implied conditional
# independencies from g on the dataset g, and reports the statistic, p-value
# and the RMSEA for each test.
options(max.print=1000000)
sink("C:/python/bn/localtests.txt")
localTests(g,d,type="cis.chisq")


