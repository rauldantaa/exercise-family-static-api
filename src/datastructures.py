class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []
        
        
        self._initialize_family()

    def _initialize_family(self):
        
        initial_members = [
            {
                "first_name": "John",
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "first_name": "Jane",
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "first_name": "Jimmy",
                "age": 5,
                "lucky_numbers": [1]
            }
        ]
        
        for member in initial_members:
            self.add_member(member)

    
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        """
        
        """
        
        if 'id' not in member or member['id'] is None:
            member['id'] = self._generate_id()
        else:
            
            if member['id'] >= self._next_id:
                self._next_id = member['id'] + 1
        
        
        member['last_name'] = self.last_name
        
        
        self._members.append(member)
        
        return member

    def delete_member(self, id):
        """
       
        """
        for i, member in enumerate(self._members):
            if member['id'] == id:
                return self._members.pop(i)
        return None

    def get_member(self, id):
        """
       
        """
        for member in self._members:
            if member['id'] == id:
                return member
        return None

    def get_all_members(self):
        """
       
        """
        return self._members