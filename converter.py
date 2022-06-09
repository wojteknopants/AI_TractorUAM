from settings import *

class Converter:
    """Can convert cartesian to isometric coordinates."""
    def __init__(self):
        self.tile_width_half = TILEWIDTH_HALF
        self.tile_height_half = TILEHEIGHT_HALF

    def convert_cart(self, x, y):
        #cart_x = x * self.tile_width_half
        #cart_y = y * self.tile_height_half
        #iso_x = cart_x - cart_y
        #iso_y = (cart_x + cart_y) / 2
        iso_x = 600 + x * 16 - y * 16 #32/2 = 16px   
        iso_y = 100 + x * 8 + y * 8 #16/2 = 8px  #600px i 100px to przesuniecie calej mapy w bok
        return iso_x, iso_y

    def convert_rect(self, rect_x, rect_y):
        cart_x = rect_x * self.tile_width_half
        cart_y = rect_y * self.tile_height_half
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2
        return iso_x, iso_y

    def isotocart(self, iso_x, iso_y):
        cart_x = (iso_x-16 + 2*iso_y - 800)/32 
        cart_y = (-iso_x + 2*iso_y + 400)/32
        return cart_x, cart_y

    def isototilenr(self, iso_x, iso_y):
        cart_x, cart_y = self.isotocart(iso_x, iso_y)
        return int(cart_x), int(cart_y)
#con = Converter()
#cx, cy = 14.99, 19.9
#ix, iy = con.convert_cart(cx,cy)
#print(ix, iy)
#rcx, rcy = isotocart(ix, iy)
#print(int(rcx), int(rcy))
