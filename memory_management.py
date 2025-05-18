class MemoryManager:
    def __init__(self, total_pages=16, page_size=1024):
        self.total_pages = total_pages
        self.page_size = page_size
        self.free_pages = list(range(total_pages))
        self.page_tables = {}

    def allocate_memory(self, pcb):
        if len(self.free_pages) >= pcb.pages_needed:
            pcb.pages = self.free_pages[:pcb.pages_needed]
            self.free_pages = self.free_pages[pcb.pages_needed:]
            self.page_tables[pcb.pid] = pcb.pages
            print(f"Allocated {pcb.pages_needed} pages to {pcb.name}: {pcb.pages}")
            return True
        else:
            print(f"Not enough memory for {pcb.name}")
            return False

    def deallocate_memory(self, pcb):
        self.free_pages.extend(pcb.pages)
        self.free_pages.sort()
        del self.page_tables[pcb.pid]
        print(f"Deallocated pages {pcb.pages} from {pcb.name}")
        pcb.pages = []

    def translate_address(self, pid, virtual_address):
        if pid not in self.page_tables:
            return None, "No page table for PID"
        pages = self.page_tables[pid]
        page = virtual_address // self.page_size
        offset = virtual_address % self.page_size
        if page >= len(pages):
            return None, "Invalid page number"
        physical_address = (pages[page] * self.page_size) + offset
        return physical_address, f"Virtual address {virtual_address} -> Physical address {physical_address} (Page {pages[page]}, Offset {offset})"