class AIPredictions():
    def getAIPredictions():
        AIpredictions = {
            "10": "22",
            "11": "50",
            "12": "40",
            "13": "76",
            "14": "70",
            "15": "64",
            "16": "30",
            "17": "37",
            "18": "90",
            "20": "27",
            "21": "28",
            "22": "56",
            "23": "59",
            "24": "95",
            "25": "20",
            "26": "28",
            "27": "61",
            "28": "71",
        } 
        return AIpredictions
    
    def getAITumorCellCount():
        AIpredictions = {
            "10": "20",
            "11": "690",
            "12": "661",
            "13": "1129",
            "14": "100",
            "15": "51",
            "16": "449",
            "17": "39",
            "18": "87",
            "20": "384",
            "21": "690",
            "22": "68",
            "23": "860",
            "24": "134",
            "25": "17",
            "26": "22",
            "27": "56",
            "28": "104",
        } 
        return AIpredictions
    
    def getAITotalCellCount():
        AIpredictions = {
            "10": "91",
            "11": "1381",
            "12": "1633",
            "13": "1482",
            "14": "142",
            "15": "80",
            "16": "1513",
            "17": "106",
            "18": "97",
            "20": "1449",
            "21": "1480",
            "22": "121",
            "23": "1448",
            "24": "141",
            "25": "86",
            "26": "78",
            "27": "92",
            "28": "142",
        } 
        return AIpredictions
    
class TrainingAIPredictions():
    def getTrainingAIPredictions():
        TrainingAIpredictions = {
            0: "53",
            1: "56",
        } 
        return TrainingAIpredictions
    
    def getTrainingAITumorCellCount():
        TrainingAIpredictions = {
            0: "72",
            1: "780",
        } 
        return TrainingAIpredictions
    
    def getTrainingAITotalCellCount():
        TrainingAIpredictions = {
            0: "137",
            1: "1382",
        } 
        return TrainingAIpredictions 
    
class GroundTruth():
    def getGroundTruth(key):
        GT = {
            "10": 30,
            "11": 44,
            "12": 63,
            "13": 72,
            "14": 19,
            "15": 15,
            "16": 22,
            "17": 61,
            "18": 88,
            "20": 28,
            "21": 49,
            "22": 60,
            "23": 71,
            "24": 14,
            "25": 11,
            "26": 20,
            "27": 55,
            "28": 87,
        } 
        return GT.get(key)