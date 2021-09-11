function sysd = augmented_model(sysc,h,d)
%AUGMENTED_MODEL Discretize a continuous-time system, with actuation delay
%   Given a continuous-time state-space system sysc, a control period h, and a
%   sensor-to-actuator delay d, this function returns an augmented state-space
%   model for the discrete-time system.
    phi = expm(sysc.A*h);
    f_phi = @(s)expm(sysc.A*s);
    Gamma0 = integral(f_phi,0,h-d, 'ArrayValued', true)*sysc.B;
    Gamma1 = integral(f_phi,h-d,h, 'ArrayValued', true)*sysc.B;
    phi_a = [phi Gamma1; zeros(size(sysc.B,2), size(sysc.A,2)+size(sysc.B,2))];
    Gamma_a = [Gamma0; eye(size(sysc.B,2))];
    C_a = [sysc.C zeros(size(sysc.C,1), size(sysc.B,2))];
    D_a = zeros(size(C_a,1), size(Gamma_a,2));
    sysd = ss(phi_a, Gamma_a, C_a, D_a, h);
end

