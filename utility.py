import datetime
import difflib
import os
import pickle
import re

import common
from geopy import distance
import string
from datetime import date, datetime, timedelta
import math
from telegram import  Update
from math import radians, cos, sin, asin, sqrt


class Utility:


    @staticmethod
    def sum_times(time1, time2):
        dt1 = datetime.datetime.combine(datetime.date.today(), time1)
        dt2 = datetime.datetime.combine(datetime.date.today(), time2)

        # somma gli oggetti datetime
        result = dt1 + dt2

        # converte il risultato in un oggetto time
        result_time = result.time()

        # stampa il risultato
        print(result_time)

    @staticmethod
    def time_plus_delta(time_obj, interval):
        delta = datetime.timedelta(minutes=interval)
        new_time = datetime.datetime.combine(datetime.date.today(), time_obj) + delta
        return new_time.time()

    @staticmethod
    def sort_arrivals(arrivals):
        sorted_arrivals = sorted(arrivals, key=lambda arrival: arrival.time)
        return sorted_arrivals

    @staticmethod
    def arrivals_to_text(arrivals_list):
        result = ''
        for arrival in arrivals_list:
            result += f'{arrival.to_text()}\n'
        return result

    @staticmethod
    def arrivals_to_brief_text(arrivals_list):
        result = ''
        for arrival in arrivals_list:
            result += f"{arrival.to_brief_text()}\n"
        return result

    @staticmethod
    def remove_duplicates(collection):
        # seen = set()
        # return [x for x in collection if not (x in seen or seen.add(x))]
        seen = set()
        result = []
        for sublist in collection:
            # Converto la sottolista in una tupla per renderla hashabile
            sublist_tuple = tuple(sublist)
            if sublist_tuple not in seen:
                result.append(sublist)
                seen.add(sublist_tuple)
        return result

    @staticmethod
    def iter_subdirectories(directory):
        for subdir, _, _ in os.walk(directory):
            yield subdir
    @staticmethod
    def formatted_date(date_str):
        return datetime.strptime(date_str, '%Y%m%d').date()

    @staticmethod
    def simplified_id(id):
        result = id
        if '_600' in result:
            result = id.split('_600')[0]
        if '@' in result:
            index = result.find('@')
            result = result[index + 1:]
        return  result

    @staticmethod
    def fixed_id(id):
        result = id
        if '_600' in result:
            result = id.split('_600')[0]
        return result

    @staticmethod
    def contains_symbols(s):
        symbols = string.punctuation
        for char in s:
            if char in symbols:
                return True
        return False

    @staticmethod
    def strings_similarity_ratio(s1,s2):
        return difflib.SequenceMatcher(None, s1, s2).ratio()

    @staticmethod
    def are_strings_similar(s1, s2, threshold):
        if Utility.strings_similarity_ratio(s1,s2) > threshold:
            return True
        else:
            return False

    @staticmethod
    def do_strings_contain_similar_word(s1, s2, threshold):
        score = Utility.word_by_word_similarity_score(s1, s2)
        if score > threshold:
            return True
        else:
            return False

    @staticmethod
    def word_by_word_similarity_score(s1, s2):
        words1 = re.split(r'[\s._/-]', s1.lower())
        words2 = re.split(r'[\s._/-]', s2.lower())

        max_similarity = 0

        for word1 in words1:
            for word2 in words2:
                if len(word1) > 3 and len(word2) > 3:
                    similarity = Utility.strings_similarity_ratio(word1, word2)
                    if similarity > max_similarity:
                        max_similarity = similarity
        return max_similarity

    @staticmethod
    def get_sorted_similar_strings(string_list, target_string, threshold):
        if len(string_list) == 0:
            return
        # Calcola il grado di somiglianza per ogni stringa nella lista rispetto alla stringa di confronto
        similarity_scores = [(string, Utility.strings_similarity_ratio(string, target_string)) for string in
                             string_list]
        result_scores = []
        for i, score in enumerate(similarity_scores):
            if score[1] >= threshold:
                result_scores.append(similarity_scores[i])
        # Ordina la lista in base alla somiglianza (dal valore più alto al valore più basso)
        sorted_strings = sorted(result_scores, key=lambda x: x[1], reverse=True)
        # Estrae solo le stringhe dalla lista ordinata
        sorted_strings = [string for string, _ in sorted_strings]
        print(sorted_strings)
        return Utility.remove_duplicates(sorted_strings)

    @staticmethod
    def sort_strings_by_similarity(string_list, target_string):
        if len(string_list) == 0:
            return
        # Calcola il grado di somiglianza per ogni stringa nella lista rispetto alla stringa di confronto
        similarity_scores = [(string, Utility.strings_similarity_ratio(string, target_string)) for string in
                             string_list]
        # Ordina la lista in base alla somiglianza (dal valore più alto al valore più basso)
        sorted_strings = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        # Estrae solo le stringhe dalla lista ordinata
        sorted_strings = [string for string, _ in sorted_strings]
        return sorted_strings

    @staticmethod
    def sort_stops_by_name_similarity(stops, target_string):

        if len(stops) == 0:
            return
        temp = []
        for stop in stops:
            temp.append((stop, difflib.SequenceMatcher(None, stop.name, target_string).ratio()))
        sorted_tuples = sorted(temp, key=lambda x: x[1], reverse=True)
        sorted_stops = []
        for tuple in sorted_tuples:
            sorted_stops.append(tuple[0])
        return sorted_stops
        

        # if len(stops) == 0:
        #     return
        # stop_names = {stop.name: stop for stop in stops}
        # print(stop_names)
        # sorted_names = Utility.sort_strings_by_similarity(stop_names, target_string)
        # print(sorted_names)
        # sorted_stops = []
        # for name in sorted_names:
        #     sorted_stops.append(stop_names[name])
        # return sorted_stops

    # @staticmethod
    # def save_objects(filename, objects):
    #     with open(filename, 'wb') as file:
    #         pickle.dump(objects, file)
    # @staticmethod
    # def load_objects(filename):
    #     with open(filename, 'rb') as file:
    #         objects = pickle.load(file)
    #     return objects
    @staticmethod
    def save_data(file_path, data):
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
            print('Dati salvati con successo.')

    @staticmethod
    def load_data(file_path):
        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                return data
        except FileNotFoundError:
            return None
        except pickle.UnpicklingError:
            return None

    @staticmethod
    def get_stop(id):
        return common.stops_dict[id]

    @staticmethod
    def get_current_date_str():
        today = date.today()
        formatted_date = today.strftime("%Y-%m-%d")
        return formatted_date

    @staticmethod
    def get_now_plus_deltamins(delta):
        current_time = datetime.now()
        delta_minutes = timedelta(minutes=delta)
        new_time = current_time + delta_minutes
        print(new_time.strftime('%H:%M:%S'))
        return new_time.strftime('%H:%M:%S')


    @staticmethod
    def get_trip(id):
        return common.trips_dict[id]

    @staticmethod
    def get_line(number):
        return common.lines_dict[number]

    @staticmethod
    def sort_stops_by_dist_to(stops, lat, lon):
        sorted_stops = sorted(stops, key=lambda stop: Utility.haversine(lat, lon, stop.latitude, stop.longitude))
        return sorted_stops

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        # Conversione delle latitudini e longitudini in radianti
        lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

        # Calcolo delle differenze di latitudine e longitudine
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Calcolo della distanza utilizzando la formula di Haversine
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Raggio medio della Terra in chilometri
        distance = c * r

        return distance
    @staticmethod
    def distance(lat1, lon1, lat2, lon2):
        # Calcolo della distanza tra due coordinate utilizzando la formula di Haversine
        R = 6371  # Raggio della Terra in chilometri

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance
    @staticmethod
    def timeObj(str):
        time_format = "%H:%M:%S"
        time_obj = datetime.strptime(str, time_format).time()
        return time_obj


    # @staticmethod
    # def user_position(update: Update, context):
    #     context.bot.send_message(chat_id=update.effective_chat.id,
    #                              text="Per favore, condividi la tua posizione per ottenere le coordinate.")