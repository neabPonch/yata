"""
Copyright 2019 kivou.2000607@gmail.com

This file is part of yata.

    yata is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    yata is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with yata. If not, see <https://www.gnu.org/licenses/>.
"""

from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from bazaar.models import Item
from bazaar.models import BazaarData
from bazaar.models import AbroadStocks
from player.models import Player
from yata.handy import apiCall
from yata.handy import returnError
from yata.handy import timestampToDate
from yata.handy import tsnow


def index(request):
    try:
        if request.session.get('player'):
            print('[view.bazaar.index] get player id from session')
            tId = request.session["player"].get("tId")
        else:
            print('[view.bazaar.index] anon session')
            tId = -1

        player = Player.objects.filter(tId=tId).first()
        player.lastActionTS = int(timezone.now().timestamp())
        player.active = True
        key = player.getKey()
        bazaarJson = json.loads(player.bazaarJson)
        playerList = bazaarJson.get("list", [])
        player.bazaarInfo = "{}".format(len(playerList))

        # update inventory of bazaarJson
        error = False
        if tId > 0:
            invtmp = apiCall("user", "", "inventory,display,bazaar", key)
            for k, v in invtmp.items():
                if v is None:
                    invtmp[k] = dict({})
            if 'apiError' in invtmp:
                error = invtmp
            else:
                bazaarJson["inventory"] = {str(v["ID"]): v["quantity"] for v in invtmp.get("inventory", dict({}))}
                bazaarJson["bazaar"] = {str(v["ID"]): v["quantity"] for v in invtmp.get("bazaar", dict({}))}
                bazaarJson["display"] = {str(v["ID"]): v["quantity"] for v in invtmp.get("display", dict({}))}
                player.bazaarJson = json.dumps(bazaarJson)

        player.save()

        print('[view.bazaar.default] get all items on market')
        itemsOnMarket = Item.objects.filter(onMarket=True).order_by('tName')
        print('[view.bazaar.default] get all tTypes')
        tTypes = [r["tType"] for r in itemsOnMarket.values("tType").distinct()]
        # print('[view.bazaar.default] {}'.format(tTypes))
        print('[view.bazaar.default] create output items')
        items = {tType: [] for tType in tTypes}

        inventory = bazaarJson.get("inventory", dict({}))
        bazaar = bazaarJson.get("bazaar", dict({}))
        display = bazaarJson.get("display", dict({}))
        for tType in items:
            for item in itemsOnMarket.filter(tType=tType):
                item.stockI = inventory.get(str(item.tId), 0)
                item.stockB = bazaar.get(str(item.tId), 0)
                item.stockD = display.get(str(item.tId), 0)
                item.stock = item.stockI + item.stockB + item.stockD
                items[tType].append(item)
                # item.save()

        context = {"player": player, 'list': playerList, "bazaarcat": True, "allItemsOnMarket": items, "view": {"refreshType": True, "timer": True, "hideType": True, "loopType": True}}
        if error:
            context.update(error)
        return render(request, 'bazaar.html', context)

        # else:
        #     return returnError(type=403, msg="You might want to log in.")

    except Exception as e:
        return returnError(exc=e, session=request.session)


def custom(request):
    try:
        if request.session.get('player'):
            print('[view.bazaar.default] get player id from session')
            tId = request.session["player"].get("tId")
            player = Player.objects.filter(tId=tId).first()
            player.lastActionTS = int(timezone.now().timestamp())
            player.save()

            bazaarJson = json.loads(player.bazaarJson)
            playerList = bazaarJson.get("list", [])

            print('[view.bazaar.default] get all items on player\'s list')
            itemsOnMarket = Item.objects.filter(tId__in=playerList).order_by('tName')
            print('[view.bazaar.default] create output items')
            items = {"Custom": []}

            inventory = bazaarJson.get("inventory", dict({}))
            bazaar = bazaarJson.get("bazaar", dict({}))
            display = bazaarJson.get("display", dict({}))
            for item in itemsOnMarket:
                item.stockI = inventory.get(str(item.tId), 0)
                item.stockB = bazaar.get(str(item.tId), 0)
                item.stockD = display.get(str(item.tId), 0)
                item.stock = item.stockI + item.stockB + item.stockD
                items["Custom"].append(item)
                # item.save()

            context = {"player": player, 'list': playerList, "bazaarcat": True, "allItemsOnMarket": items, "view": {"refreshType": True, "timer": True, "loopType": True}}
            page = 'bazaar/content-reload.html' if request.method == 'POST' else "bazaar.html"
            return render(request, page, context)
        else:
            return returnError(type=403, msg="You might want to log in.")

    except Exception as e:
        return returnError(exc=e, session=request.session)


def default(request):
    try:
        if request.session.get('player'):
            print('[view.bazaar.default] get player id from session')
            tId = request.session["player"].get("tId")
        else:
            print('[view.bazaar.default] anon session')
            tId = -1

        player = Player.objects.filter(tId=tId).first()
        player.lastActionTS = int(timezone.now().timestamp())
        player.save()

        bazaarJson = json.loads(player.bazaarJson)
        playerList = bazaarJson.get("list", [])

        print('[view.bazaar.default] get all items on market')
        itemsOnMarket = Item.objects.filter(onMarket=True).order_by('tName')
        print('[view.bazaar.default] get all tTypes')
        tTypes = [r["tType"] for r in itemsOnMarket.values("tType").distinct()]
        # print('[view.bazaar.default] {}'.format(tTypes))
        print('[view.bazaar.default] create output items')
        items = {tType: [] for tType in tTypes}

        inventory = bazaarJson.get("inventory", dict({}))
        bazaar = bazaarJson.get("bazaar", dict({}))
        display = bazaarJson.get("display", dict({}))
        for tType in items:
            for item in itemsOnMarket.filter(tType=tType):
                item.stockI = inventory.get(str(item.tId), 0)
                item.stockB = bazaar.get(str(item.tId), 0)
                item.stockD = display.get(str(item.tId), 0)
                item.stock = item.stockI + item.stockB + item.stockD
                items[tType].append(item)
                # item.save()

        context = {"player": player, 'list': playerList, "bazaarcat": True, "allItemsOnMarket": items, "view": {"refreshType": True, "timer": True, "hideType": True, "loopType": True}}
        page = 'bazaar/content-reload.html' if request.method == 'POST' else "bazaar.html"
        return render(request, page, context)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def sets(request):
    try:
        if request.session.get('player'):
            print('[view.bazaar.sets] get player id from session')
            tId = request.session["player"].get("tId")
        else:
            print('[view.bazaar.sets] anon session')
            tId = -1

        player = Player.objects.filter(tId=tId).first()
        player.lastActionTS = int(timezone.now().timestamp())
        player.save()

        bazaarJson = json.loads(player.bazaarJson)
        playerList = bazaarJson.get("list", [])

        print('[view.bazaar.default] get all items on market')
        itemsOnMarket = Item.objects.filter(onMarket=True).order_by('tName')
        print('[view.bazaar.default] get all tTypes')
        tTypes = ["Flower", "Plushie"]
        # print('[view.bazaar.default] {}'.format(tTypes))
        print('[view.bazaar.default] create output items')
        items = {tType: [] for tType in tTypes}

        inventory = bazaarJson.get("inventory", dict({}))
        bazaar = bazaarJson.get("bazaar", dict({}))
        display = bazaarJson.get("display", dict({}))
        for tType in items:
            for item in itemsOnMarket.filter(tType=tType):
                item.stockI = inventory.get(str(item.tId), 0)
                item.stockB = bazaar.get(str(item.tId), 0)
                item.stockD = display.get(str(item.tId), 0)
                item.stock = item.stockI + item.stockB + item.stockD
                items[tType].append(item)
                # item.save()

        context = {"player": player, 'list': playerList, "bazaarcat": True, "allItemsOnMarket": items, "view": {"refreshType": True, "timer": True, "loopType": True}}
        page = 'bazaar/content-reload.html' if request.method == 'POST' else "bazaar.html"
        return render(request, page, context)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def all(request):
    try:
        if request.session.get('player'):
            print('[view.bazaar.all] get player id from session')
            tId = request.session["player"].get("tId")
        else:
            print('[view.bazaar.all] anon session')
            tId = -1

        player = Player.objects.filter(tId=tId).first()
        player.lastActionTS = int(timezone.now().timestamp())
        player.save()

        bazaarJson = json.loads(player.bazaarJson)
        playerList = bazaarJson.get("list", [])

        print('[view.bazaar.default] get all items on market')
        itemsOnMarket = Item.objects.all().order_by('tName')
        print('[view.bazaar.default] get all tTypes')
        tTypes = [r["tType"] for r in itemsOnMarket.values("tType").distinct()]
        # print('[view.bazaar.default] {}'.format(tTypes))
        print('[view.bazaar.default] create output items')
        items = {tType: [] for tType in tTypes}

        inventory = bazaarJson.get("inventory", dict({}))
        bazaar = bazaarJson.get("bazaar", dict({}))
        display = bazaarJson.get("display", dict({}))
        for tType in items:
            for item in itemsOnMarket.filter(tType=tType):
                item.stockI = inventory.get(str(item.tId), 0)
                item.stockB = bazaar.get(str(item.tId), 0)
                item.stockD = display.get(str(item.tId), 0)
                item.stock = item.stockI + item.stockB + item.stockD
                items[tType].append(item)
                # item.save()

        context = {"player": player, 'list': playerList, "bazaarcat": True, "allItemsOnMarket": items, "view": {"hideType": True, "loopType": True}}
        page = 'bazaar/content-reload.html' if request.method == 'POST' else "bazaar.html"
        return render(request, page, context)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def top10(request):
    try:
        if request.session.get('player'):
            print('[view.bazaar.top10] get player id from session')
            tId = request.session["player"].get("tId")
        else:
            print('[view.bazaar.top10] anon session')
            tId = -1

        player = Player.objects.filter(tId=tId).first()
        player.lastActionTS = int(timezone.now().timestamp())
        player.save()

        bazaarJson = json.loads(player.bazaarJson)
        playerList = bazaarJson.get("list", [])

        print('[view.bazaar.default] create output items')
        items = {"Sell": [], "Buy": []}

        inventory = bazaarJson.get("inventory", dict({}))
        bazaar = bazaarJson.get("bazaar", dict({}))
        display = bazaarJson.get("display", dict({}))
        for item in Item.objects.filter(onMarket=True).order_by('weekTendency')[:10]:
            item.stockI = inventory.get(str(item.tId), 0)
            item.stockB = bazaar.get(str(item.tId), 0)
            item.stockD = display.get(str(item.tId), 0)
            item.stock = item.stockI + item.stockB + item.stockD
            items["Buy"].append(item)
            # item.save()
        for item in Item.objects.filter(onMarket=True).order_by('-weekTendency')[:10]:
            item.stockI = inventory.get(str(item.tId), 0)
            item.stockB = bazaar.get(str(item.tId), 0)
            item.stockD = display.get(str(item.tId), 0)
            item.stock = item.stockI + item.stockB + item.stockD
            items["Sell"].append(item)
            # item.save()

        context = {"player": player, 'list': playerList, "bazaarcat": True, "allItemsOnMarket": items, "view": {"refreshType": True, "timer": True, "loopType": True}}
        page = 'bazaar/content-reload.html' if request.method == 'POST' else "bazaar.html"
        return render(request, page, context)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def details(request, itemId):
    try:
        if request.method == "POST":
            item = Item.objects.filter(tId=itemId).first()

            context = {'item': item}
            return render(request, 'bazaar/details.html', context)

        else:
            message = "You might want to log in." if request.method == "POST" else "You need to post. Don\'t try to be a smart ass."
            return returnError(type=403, msg=message)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def prices(request, itemId):
    try:
        if request.method == "POST":
            item = Item.objects.filter(tId=itemId).first()

            # create price histogram
            priceHistory = sorted(json.loads(item.priceHistory).items(), key=lambda x: x[0])
            # plot only last 8 points of the Tendency
            graph = [[t, p, item.weekTendencyA * float(t) + item.weekTendencyB, item.monthTendencyA * float(t) + item.monthTendencyB] for t, p in priceHistory]
            graphLength = 0
            maxTS = priceHistory[-1][0]
            for i, (t, p, wt, mt) in enumerate(graph):
                if not int(p):
                    graph[i][1] = "null"
                    # graph[i][2] = "null"
                    # graph[i][3] = "null"
                else:
                    graphLength += 1
                if int(maxTS) - int(t) > 3600 * 24 * 7 or wt < 0:
                    graph[i][2] = "null"
                if int(maxTS) - int(t) > 3600 * 24 * 31 or mt < 0:
                    graph[i][3] = "null"

                # convert timestamp to date
                graph[i][0] = timestampToDate(int(t))

            context = {'item': item, "graph": graph, "graphLength": graphLength}
            return render(request, 'bazaar/prices.html', context)

        else:
            message = "You might want to log in." if request.method == "POST" else "You need to post. Don\'t try to be a smart ass."
            return returnError(type=403, msg=message)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def update(request, itemId):
    try:
        if request.session.get('player') and request.method == "POST":
            print('[view.bazaar.updateItem] get player id from session')
            tId = request.session["player"].get("tId")
            player = Player.objects.filter(tId=tId).first()
            key = player.getKey()
            bazaarJson = json.loads(player.bazaarJson)
            playerList = bazaarJson.get("list", [])

            print('[view.bazaar.updateItem] get item')
            item = Item.objects.filter(tId=itemId).first()
            print('[view.bazaar.updateItem] {}'.format(item))

            baz = item.update_bazaar(key=key, n=BazaarData.objects.first().nItems)
            error = False
            if 'apiError' in baz:
                error = baz

            # update inventory of bazaarJson
            error = False
            invtmp = apiCall("user", "", "inventory,display,bazaar", key)
            for k, v in invtmp.items():
                if v is None:
                    invtmp[k] = dict({})
            if 'apiError' in invtmp:
                error = {"apiErrorSub": invtmp["apiError"]}
            else:
                # modify user
                bazaarJson["inventory"] = {str(v["ID"]): v["quantity"] for v in invtmp.get("inventory", dict({}))}
                bazaarJson["bazaar"] = {str(v["ID"]): v["quantity"] for v in invtmp.get("bazaar", dict({}))}
                bazaarJson["display"] = {str(v["ID"]): v["quantity"] for v in invtmp.get("display", dict({}))}
                item.stockI = bazaarJson["inventory"].get(str(item.tId), 0)
                item.stockB = bazaarJson["bazaar"].get(str(item.tId), 0)
                item.stockD = bazaarJson["display"].get(str(item.tId), 0)
                item.stock = item.stockI + item.stockB + item.stockD
                # item.save()

            player.bazaarJson = json.dumps(bazaarJson)
            player.save()

            context = {'player': player, 'list': playerList, 'item': item, "view": {"timer": True}}
            if error:
                context.update(error)
            return render(request, "bazaar/item.html", context)

        else:
            message = "You might want to log in." if request.method == "POST" else "You need to post. Don\'t try to be a smart ass."
            return returnError(type=403, msg=message)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def delete(request, itemId):
    try:
        if request.session.get('player') and request.method == "POST":

            print('[view.bazaar.deleteItem] delete item')
            item = Item.objects.filter(tId=itemId).first()
            item.lastUpdateTS = 0
            item.marketdata_set.all().delete()
            item.save()

            context = {'item': item, "view": {"timer": True}}
            return render(request, "bazaar/item.html", context)

        else:
            message = "You might want to log in." if request.method == "POST" else "You need to post. Don\'t try to be a smart ass."
            return returnError(type=403, msg=message)

    except Exception as e:
        return returnError(exc=e, session=request.session)


def toggle(request, itemId):
    try:
        if request.session.get('player') and request.method == "POST":
            print('[view.bazaar.updateItem] get player id from session')
            tId = request.session["player"].get("tId")
            player = Player.objects.filter(tId=tId).first()
            bazaarJson = json.loads(player.bazaarJson)
            playerList = bazaarJson.get("list", [])

            item = Item.objects.filter(tId=itemId).first()
            if itemId in playerList:
                playerList.remove(itemId)
            else:
                playerList.append(itemId)

            item.stockI = bazaarJson["inventory"].get(str(item.tId), 0)
            item.stockB = bazaarJson["bazaar"].get(str(item.tId), 0)
            item.stockD = bazaarJson["display"].get(str(item.tId), 0)
            item.stock = item.stockI + item.stockB + item.stockD

            bazaarJson["list"] = playerList
            player.bazaarJson = json.dumps(bazaarJson)
            player.save()

            context = {'player': player, 'item': item, 'list': playerList, "view": {"timer": True}}
            return render(request, "bazaar/item.html", context)

        else:
            message = "You might want to log in." if request.method == "POST" else "You need to post. Don\'t try to be a smart ass."
            return returnError(type=403, msg=message)

    except Exception as e:
        return returnError(exc=e, session=request.session)


@csrf_exempt
def abroadImport(request):
    from bazaar.countries import countries

    if request.method == 'POST':
        try:
            payload = json.loads(request.body)

            # check mandatory keys
            for key in ["country", "items"]:
                if key not in payload:
                    return JsonResponse({"message": "Missing \'{}\' key in payload".format(key)}, status=400)

            # check items length
            if not len(payload["items"]):
                return JsonResponse({"message": "Empty items list"}, status=400)

            # check country:
            country_key = str(payload["country"]).lower().strip()[:3]
            if country_key not in countries:
                return JsonResponse({"message": "Unknown country key {}".format(country_key)}, status=400)

            country = countries[country_key]["name"]
            items = payload["items"]
            # uid = int(payload.get("uid", 0)) if str(payload.get("uid", 0)).isdigit() else 0
            client = payload.get("client", "unknown").strip()
            timestamp = tsnow()

            # convert list to dict and check keys
            if isinstance(items, list):
                items_list = items
                items = dict({})
                for item in items_list:
                    for key in ["id", "quantity", "cost"]:
                        if not str(item.get(key)).isdigit():
                            return JsonResponse({"message": "Wrong {} for item object: {}".format(key, item.get(key))}, status=400)
                    items[item["id"]] = {"cost": item["cost"], "quantity": item["quantity"]}

            elif isinstance(items, dict):
                for item_id, item in items.items():
                    for key in ["quantity", "cost"]:
                        if not str(item.get(key)).isdigit():
                            return JsonResponse({"message": "Wrong item {} for item {}".format(key, item_id)}, status=400)

            else:
                return JsonResponse({"message": "Wrong item list format {}".format(type(items))}, status=400)

            # get all unique items from this country
            distinct_items = [k['item_id'] for k in AbroadStocks.objects.filter(country_key=country_key).values('item_id').distinct()]

            # add items not in db
            for k in items:
                if int(k) not in distinct_items:
                    distinct_items.append(int(k))

            stocks = dict({})
            for item_id in distinct_items:
                item = items.get(str(item_id), False)
                cost = 0
                quantity = 0
                if item:
                    cost = int(item["cost"])
                    quantity = int(item["quantity"])
                else:
                    lastItem = AbroadStocks.objects.filter(item_id=item_id, country_key=country_key).order_by("-timestamp").first()
                    cost = 0 if lastItem is None else lastItem.cost
                    quantity = 0

                stocks[item_id] = {"country": country,
                                   "country_key": country_key,
                                   "client": client,
                                   "timestamp": timestamp,
                                   "cost": cost,
                                   "quantity": quantity}

            for k, v in stocks.items():
                item = Item.objects.filter(tId=k).first()
                if item is None:
                    return JsonResponse({"message": "Item {} not found in database".format(k)}, status=400)

                AbroadStocks.objects.filter(item=item, country_key=v["country_key"], last=True).update(last=False)
                v["last"] = True
                item.abroadstocks_set.create(**v)

            return JsonResponse({"message": "success", "stocks": stocks}, status=200)

        except BaseException as e:
            return JsonResponse({"message": "Server error: {}".format(e)}, status=500)

    else:
        return returnError(type=403, msg="Expecting a POST request.")


def abroadExport(request):
    from bazaar.countries import countries

    try:

        # get all last stocks
        stocksDB = AbroadStocks.objects.filter(last=True)

        # filter by type
        if request.GET.get("type", False):
            print("Filter", request.GET.get("type", False))
            type = str(request.GET.get("type")).strip().title()
            if type not in ["Drug", "Plushie", "Flower"]:
                return JsonResponse({"message": "Unknown type {}".format(type)}, status=400)
            stocksDB = stocksDB.filter(item__tType=type)

        # filter by country
        if request.GET.get("country", False):
            print("Filter", request.GET.get("country", False))
            country_key = str(request.GET.get("country")).lower().strip()[:3]
            if country_key not in countries:
                return JsonResponse({"message": "Unknown country key {}".format(country_key)}, status=400)
            stocksDB = stocksDB.filter(country_key=country_key)

        if request.GET.get("format", False):

            # select the format
            format = request.GET.get("format")
            if format == "country":
                stocksJS = dict({})
                for stock in stocksDB:
                    if stock.country_key not in stocksJS:
                        stocksJS[stock.country_key] = dict({})
                    stocksJS[stock.country_key][stock.item.tId] = stock.payload()

            elif format == "item":
                stocksJS = dict({})
                for stock in stocksDB:
                    if stock.item.tId not in stocksJS:
                        stocksJS[stock.item.tId] = dict({})
                    stocksJS[stock.item.tId][stock.country_key] = stock.payload()

            elif format == "flat":
                stocksJS = dict({})
                for stock in stocksDB:
                    id_b = "{}_{}".format(stock.item.tId,  stock.country_key)
                    stocksJS[id_b] = stock.payload()
            else:
                return JsonResponse({"message": "Unknown format {}".format(format)}, status=400)

        else:

            # default the format
            stocksJS = []
            for stock in stocksDB:
                stocksJS.append(stock.payload())

        return JsonResponse({"stocks": stocksJS}, status=200)

    except BaseException as e:
        return JsonResponse({"message": "Server error: {}".format(e)}, status=500)


def abroad(request):
    try:
        # build up filters list
        from bazaar.countries import countries as country_list
        from bazaar.countries import types as type_list
        country_list["all"] = {"name": "All", "n": 0}
        type_list["all"] = {"name": "All", "n": 0}
        for k, v in country_list.items():
            v["n"] = 0
        for k, v in type_list.items():
            v["n"] = 0

        # get player and page
        if request.session.get('player'):
            tId = request.session["player"].get("tId")
        else:
            tId = -1
        player = Player.objects.filter(tId=tId).first()
        page = 'bazaar/content-reload.html' if request.method == 'POST' else "bazaar.html"

        # get filters
        filters = request.session.get('stocks-filters', {"countries": "all", "types": "all"})
        if request.POST.get("filter", False) and request.POST.get("key"):
            page = "bazaar/abroad/list.html"
            post_filter = request.POST.get("filter")
            post_key = request.POST.get("key")
            if post_filter in "types" and post_key in type_list:
                filters[post_filter] = post_key if post_key != filters[post_filter] else "all"
            elif post_filter in "countries" and post_key in country_list:
                filters[post_filter] = post_key if post_key != filters[post_filter] else "all"
        request.session["stocks-filters"] = filters

        # get all stocks
        stocks = AbroadStocks.objects.filter(last=True)
        for stock in stocks:
            country_list[stock.country_key]["n"] += 1
            country_list["all"]["n"] += 1
            if stock.item.tType in ["Drug", "Plushie", "Flower"]:
                type_list[stock.item.tType]["n"] += 1
            type_list["all"]["n"] += 1

        if filters["countries"] != "all":
            stocks = stocks.filter(country_key=filters["countries"])
        if filters["types"] != "all":
            stocks = stocks.filter(item__tType=filters["types"])

        # add fields
        for stock in stocks:
            stock.profit = stock.item.tMarketValue - stock.cost
            stock.profitperhour = round(30 * stock.profit / stock.get_country()["fly_time"])
            stock.update = tsnow() - stock.timestamp

        import time
        time.sleep(0.2)
        context = {"player": player,
                   "filters": filters,
                   "country_list":country_list,
                   "type_list": type_list,
                   "stocks": stocks,
                   "bazaarcat": True,
                   "view": {"abroad": True}}

        return render(request, page, context)

    except Exception as e:
        del request.session["stocks-filters"]
        return returnError(exc=e, session=request.session)


def abroadStocks(request):
    try:
        if request.method == "POST":
            item_id = request.POST.get('item_id', False)
            country_key = request.POST.get('country_key', False)
            stocks = AbroadStocks.objects.filter(country_key=country_key, item__tId=item_id).order_by("-timestamp")

            if stocks is None:
                context = {'item': None, "graph": [], "graphLength": 0}
                return render(request, 'bazaar/abroad/graph.html', context)
                return returnError(type=403)

            # create price histogram
            # plot only last 8 points of the Tendency
            graph = [[timestampToDate(s.timestamp), s.quantity, s.cost] for s in stocks]

            context = {'item': stocks.first().item, "graph": graph}
            return render(request, 'bazaar/abroad/graph.html', context)

        else:
            message = "You might want to log in." if request.method == "POST" else "You need to post. Don\'t try to be a smart ass."
            return returnError(type=403, msg=message)

    except Exception as e:
        return returnError(exc=e, session=request.session)
