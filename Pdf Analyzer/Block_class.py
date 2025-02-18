class Block_class:
    def __init__(self, block_type, position, text, page, idx,original_idx,outline_level, outline_idx = None):
        self.type = block_type    # Text margin equation title authors sources legend
        self.position = position  # Tuple (x0, y0, x1, y1)
        self.text = text
        self.page = page
        self.tag = 'on'
        self.merged = False
        self.idx = idx            # Current id on the pdf, take into account the merges, interger
        self.original_idx  = original_idx        # Original Ids before merging, [integers]
        self.outline_level = outline_level
        self.outline_idx = outline_idx
        

    def __repr__(self):
        #return f"Block(type={self.type}, position={self.position}, text={self.text}, page ={self.page}, tag ={self.tag}, merged = {self.merged}), idx = {self.idx}, original_idx = {self.original_idx}"
        #return f"Block(type={self.type}, page ={self.page}, merged = {self.merged}, idx = {self.idx}, original_idx = {self.original_idx})\n"
        #return f"Block(type={self.type}, position={self.position}, page ={self.page}, tag ={self.tag}, merged = {self.merged}), idx = {self.idx}, original_idx = {self.original_idx}"
        #return f"Block(page ={self.page},idx = {self.idx}, original_idx = {self.original_idx}\n)"
        return(f"Block(type={self.type},\n(Text = {self.text},\nidx = {self.idx})")