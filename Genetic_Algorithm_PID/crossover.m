function [child1,child2] = crossover(str_parent1,str_parent2)
%CROSSOVER Creates a crossover of two parents
%   Uses 1 point crossover on two parent chromosones

parent1 = char(str_parent1); % They are passed in as strings
parent2 = char(str_parent2);

if length(parent1) ~= length(parent2)
    error('The parent chromozones do not match in length')
end
i = randi(length(parent1)-1); % -1 as we want some mutation always
child1 = [parent1(1:i),parent2(i+1:end)];
child2 = [parent2(1:i),parent1(i+1:end)]; % Still need to test this

end

