function [cropped_im, ov] = jitter_imcrop(im, rect, IoU)
% im: input whole image
% rect: [horizontal pos of top-left point, vertical pos of top-left point,
%        width of box, height of box]
% IoU: 0~1 intersection-area/union-area
    w = size(im,2);
    h = size(im,1);
    bbox_w = rect(3);
    bbox_h = rect(4);
    assert(rect(1) > 0 && rect(1) < w);
    assert(rect(2) > 0 && rect(2) < h);
    assert(rect(3) <= w);
    assert(rect(4) <= h);

    % original imcrop
    if IoU >= 1
        cropped_im = imcrop(im, rect);
        return;
    end
    
    % jittered crop to make IoU >= input IoU
    assert(IoU > 0 && IoU < 1);
    jrect = rect;
    % horizontal position of top-left point
    b = (1-IoU);
    a = (1-1/IoU);
    while 1
        r = a + (b-a).*rand(4,1);
        jrect(1) = max(min(rect(1) + r(1)*bbox_w, w), 1);
        jrect(2) = max(min(rect(2) + r(2)*bbox_h, h), 1);
        jrect(3) = max(min(rect(3) + r(3)*bbox_w, w), 1);
        jrect(4) = max(min(rect(4) + r(4)*bbox_h, h), 1);
        jrect = round(jrect);
        ov = box_overlap([rect(1),rect(2),rect(1)+rect(3)-1,rect(2)+rect(4)-1],...
        [jrect(1),jrect(2),jrect(1)+jrect(3)-1,jrect(2)+jrect(4)-1]);
        if ov > IoU
            break;
        end
    end
    cropped_im = imcrop(im, jrect);
end
