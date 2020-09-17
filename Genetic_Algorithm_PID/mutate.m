function [newchrom] = mutate(oldchrom)
%MUTATE Mutates a chromozones
%   Bit wise mutation of chromozone with a 0.25 probability
mutation_prob = 0.25;
% newchrom = zeros(1,length(oldchrom));
oldchrom = char(oldchrom);
for i = 1:length(oldchrom)
    if rand() < mutation_prob
        % Flip bit
        if oldchrom(i) == '1'
            newchrom(i) = '0';
        else
            newchrom(i) = '1';
        end
    else
        newchrom(i) = oldchrom(i);
    end
end

