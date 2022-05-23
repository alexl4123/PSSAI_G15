% Test for using ASP for solving the problem
#show totalcost/1.

% --------------PROGRAM-------------------

1 <= {x(A,B,0..1)} <= 1 :- c(A,B,C).

:- x(X1, X2, X12), x(X2, X1, X21), X12 + X21 < 1.

s(X, SUM1, SUM2) :- v(X), SUM1 = #sum{X12,X2 : x(X,X2,X12)}, SUM2 = #sum{X21,X1 : x(X1, X, X21)}.

:- s(X, SUM1, SUM2), DIF = SUM1 - SUM2, DIF != 0.

rc(X1,X2,RC12) :- x(X1,X2,X12), c(X1,X2,C12), RC12 = X12 * C12.
totalcost(C) :- C = #sum{RC12,X1,X2 : rc(X1,X2,RC12)}.

