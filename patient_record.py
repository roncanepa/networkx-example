class PatientRecord:
    def __init__(self, line_array):
        self.PatientId = line_array[0]
        self.PrescriberId = line_array[1]
        # line_array[4] needs to be created via parsing and passed in
        self.FillDate = line_array[4]
        self.ndc = line_array[3]

    def __str__(self):
        return "\n==Printing PatientRecord==\n\tpatientId: %s \n\tprescriberid: %s \n\tFillDate: %s \n\tndc: %s" % (self.PatientId, self.PrescriberId, self.FillDate, self.ndc)
