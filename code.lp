% Generating requests and which edges will be used

1 {chosen(R) : request(R,_,_)}. 
{use(R,A,B)} :- chosen(R), edge(A,B). 

% Preventing two different routes using the same edge
:- use(R1, N, M), use(R2, N, M), R1 != R2. 
:- use(R1, N, M), use(R2, M, N), R1 != R2.

% A chosen request needs to have a least one edge
:- chosen(R), not use(R,_,_).

% Prevents the same request from using the same edge more than once
:- use(R,N,M), use(R,M,N).

%  Prevents branching  
:- use(R, N1, M), use(R, N2, M), N1 != N2.
:- use(R, N, M1), use(R, N, M2), M1 != M2.


% No incoming edge to the start
:- request(R,N,_), use(R,_,M), N = M.

% No outgoing edge to the end
:- request(R,_,N), use(R,M,_), N = M.

% Makes sure that any used edge contains a path to the end
:- use(R,N,M), request(R,_,Y), N != Y, not path(R,N,Y). 

% Makes sure that for any used edge there is path from the start to that edge
:- use(R,N,M), request(R,Y,_), N != Y, not path(R,Y,N).

% Builds a path for a request on the edges it uses
path(R,X,Y) :- use(R,X,Y).
path(R,X,Z) :- path(R,X,Y), use(R,Y,Z).

% Maximises the number of chosen requests
#maximize {1, R : chosen(R)}.

#show use/3.
#show chosen/1.
