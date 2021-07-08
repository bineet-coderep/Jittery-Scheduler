function [y, t, x] = hold_and_skip_next(sysd,K,n,seq,x_0)
%HOLD_AND_SKIP_NEXT Hold & Skip-Next simulation, following Maggio et al. (2020)
%   This function uses a slightly different model for the hit matrices from the
%   one found in the paper.  It is modified to accept controllers that use
%   feedback from the last control input as well as the state.  This shows up as
%   non-zero values in the bottom-right-most r by r block of the hit matrices.
%   sysd: Discrete-time state-space model
%   K: Full-state feedback controller for sysd
%   n: Maximum number of deadline misses allowed
%   seq: Binary vector representing hits and misses
%   x_0: Initial condition for simulation
%
%   Maggio, Martina, et al. "Control-system stability under consecutive
%   deadline misses constraints." ECRTS 2020.

p = size(sysd.A, 1);
r = size(sysd.B, 2);

% Miss matrix
A_M = vertcat([sysd.A  zeros(p, n*p)  sysd.B], ...
              [eye(n*p)  zeros(n*p, p+r)], ...
              [zeros(r, (n+1)*p)  eye(r)]);

% Hit matrices
K_x = -K(:,1:p);
if size(K, 2) == p + r
    K_u = -K(:,p+1:p+r);
else
    K_u = zeros(p, r);
end

A_R = zeros((n+1)*p + r, (n+1)*p + r, n+1);
for i = 1:n+1
    A_R(:,:,i) = vertcat([sysd.A  zeros(p, n*p)  sysd.B], ...
                         [eye(n*p)  zeros(n*p, p+r)], ...
                         [zeros(r, (i-1)*p)  K_x  zeros(r, (n-i+1)*p)  K_u]);
end

% Simulate
x_0 = vertcat(x_0, zeros(p*n + r, 1));
t_max = size(seq, 2);
t_since_last_hit = 1;
x = zeros(p*(n+1) + r, t_max + 1);
x(:,1) = x_0;
for t = 2:t_max + 1
    if seq(t-1) == 1
        % Hit
        A = A_R(:,:,t_since_last_hit);
        t_since_last_hit = 1;
    else
        % Miss
        A = A_M;
        t_since_last_hit = t_since_last_hit + 1;
    end
    x(:,t) = A * x(:,t-1);
end
x = x(1:p,:);

% TODO
y = 0;
t = 0;
x = x';
end

