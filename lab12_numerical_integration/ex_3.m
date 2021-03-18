
fun = @(x,y)1./(sqrt(x+y).*(1+x+y));
y_max = @(x) 1 - x;

%format long
res1 = integral2(fun,0,1,0,y_max,'Method','iterated');
disp("Iterated")
disp(res1)

res2 = integral2(fun,0,1,0,y_max,'Method','tiled');
disp("Tiled")
disp(res2)

%2
max = 200;
array1 = linspace(1/max,1,max);
array2 = zeros(max);

for i = 1:max  
    x = -3:i/max:3;
    y = -5:i/max:5;
    [X,Y] = meshgrid(x,y);
    Z = X.^2 + Y.^2;
    res3 = trapz(Z);
    res4 = trapz(res3);
    array2(i) = res4;
    disp(i);
    disp(res4);
end

fun = @(x,y)x.^2 +y.^2;
res5 = integral2(fun, -3, 3, -5, 5);
disp("From integral");
disp(res5);

array3 = res5*ones(max,1);
f = figure; 
p = plot(array1, array2, array1, array3);
p(1).LineWidth = 2;
p(2).Marker = '.';
ax = gca;
ax.YLim = [0 res5 * 10];



