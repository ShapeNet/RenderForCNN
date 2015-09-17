% crop according to truncationParam
function [I, top, bottom, left, right] = crop_gray(I, bgColor, truncationParam)

% get boundaries of object
[nr, nc] = size(I);
colsum = sum(I == bgColor, 1) ~= nr;
rowsum = sum(I == bgColor, 2) ~= nc;

left = find(colsum, 1, 'first');
if left == 0
    left = 1;
end
right = find(colsum, 1, 'last');
if right == 0
    right = length(colsum);
end
top = find(rowsum, 1, 'first');
if top == 0
    top = 1;
end
bottom = find(rowsum, 1, 'last');
if bottom == 0
    bottom = length(rowsum);
end

width = right - left + 1;
height = bottom - top + 1;

% strecth
dx1 = width * truncationParam(1); % left
dx2 = width * truncationParam(2); % right
dy1 = height * truncationParam(3); % top
dy2 = height * truncationParam(4); % bottom

leftnew = max([1, left + dx1]);
leftnew = min([leftnew, nc]);
rightnew = max([1, right + dx2]);
rightnew = min([rightnew, nc]);
if leftnew > rightnew
    leftnew = left;
    rightnew = right;
end

topnew = max([1, top + dy1]);
topnew = min([topnew, nr]);
bottomnew = max([1, bottom + dy2]);
bottomnew = min([bottomnew, nr]);
if topnew > bottomnew
    topnew = top;
    bottomnew = bottom;
end

left = round(leftnew); right = round(rightnew);
top = round(topnew); bottom = round(bottomnew);
I = I(top:bottom, left:right, :);
