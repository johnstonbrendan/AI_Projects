function fixed_list = removeNaN(list)
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here
srted = sort(list);
index_nan = length(srted)+1;
for i = 1:length(srted)
    if isnan(srted(i))
        index_nan = i;
        break
    end
end
fixed_list = srted(1:index_nan-1);


