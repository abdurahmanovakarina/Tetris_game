import json


class ScoreHandler:
    def __init__(self, filename):
        self.__filename = filename
        self.__last_score = 0
        self.__record_score = 0
        self.__complexity = 0
        # self.load_scores()

    def load_scores(self, complexity):
        self.__complexity = complexity
        try:
            with open(self.__filename, "r") as f:
                scores = json.load(f)
                self.__last_score = scores[str(self.__complexity)]["last_score"]
                self.__record_score = scores[str(self.__complexity)]["record_score"]
        except (IOError, KeyError, json.decoder.JSONDecodeError):
            self.__last_score = 0
            self.__record_score = 0

    def update_score(self, score, complexity):
        self.__complexity = complexity
        self.load_scores(self.__complexity)

        if score > self.__record_score:
            self.__record_score = score

        self.__last_score = score
        self.__save_scores()

    def __create_json_file(self):
        data = {}
        for lvl in range(1, self.__complexity + 1):
            data[str(lvl)] = {"last_score": 0, "record_score": 0}

        with open(self.__filename, "w") as f:
            json.dump(data, f)

    def __save_scores(self):
        try:
            with open(self.__filename, "r") as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            self.__create_json_file()
            with open(self.__filename, "r") as f:
                data = json.loads(f.read())

        data.update(
            {
                str(self.__complexity): {
                    "last_score": self.__last_score,
                    "record_score": self.__record_score,
                }
            }
        )
        # data[str(self.__complexity)]["last_score"] = self.__last_score
        # data[str(self.__complexity)]["record_score"] = self.__record_score

        with open(self.__filename, "w") as f:
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))

        # with open(self.__filename, "w") as f:
        #     json.dump(
        #         # {"last_score": self.__last_score, "record_score": self.__record_score}, f
        #         {
        #             str(self.__complexity): {
        #                 "last_score": self.__last_score,
        #                 "record_score": self.__record_score,
        #             }
        #         },
        #
        #         f,
        #     )

    def get_last_score(self, complexity) -> int:
        self.load_scores(complexity)
        return self.__last_score

    def get_record_score(self, complexity) -> int:
        self.load_scores(complexity)
        return self.__record_score


score_handler = ScoreHandler("scores.json")
