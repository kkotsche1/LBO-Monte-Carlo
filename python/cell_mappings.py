cell_mappings = {
    'Primary Case': {
        # Key P&L Drivers
        'Revenue': {
            2023: 'I123', 2024: 'J123', 2025: 'K123', 2026: 'L123', 2027: 'M123',
            2028: 'N123', 2029: 'O123', 2030: 'P123'
        },
        'EBITDA': {
            2023: 'I124', 2024: 'J124', 2025: 'K124', 2026: 'L124', 2027: 'M124',
            2028: 'N124', 2029: 'O124', 2030: 'P124'
        },
        'EBITDA normalizations': {
            2023: 'I125', 2024: 'J125', 2025: 'K125', 2026: 'L125', 2027: 'M125',
            2028: 'N125', 2029: 'O125', 2030: 'P125'
        },
        'Depreciation': {
            2023: 'I126', 2024: 'J126', 2025: 'K126', 2026: 'L126', 2027: 'M126',
            2028: 'N126', 2029: 'O126', 2030: 'P126'
        },
        'Amortization': {
            2023: 'I127', 2024: 'J127', 2025: 'K127', 2026: 'L127', 2027: 'M127',
            2028: 'N127', 2029: 'O127', 2030: 'P127'
        },
        'EBIT': {
            2023: 'I128', 2024: 'J128', 2025: 'K128', 2026: 'L128', 2027: 'M128',
            2028: 'N128', 2029: 'O128', 2030: 'P128'
        },
        # CapEx
        'Maintenance Capex': {
            2023: 'I131', 2024: 'J131', 2025: 'K131', 2026: 'L131', 2027: 'M131',
            2028: 'N131', 2029: 'O131', 2030: 'P131'
        },
        'Expansion Capex': {
            2023: 'I132', 2024: 'J132', 2025: 'K132', 2026: 'L132', 2027: 'M132',
            2028: 'N132', 2029: 'O132', 2030: 'P132'
        },
        # Balance Sheet Items
        'Inventory': {
            2023: 'I135', 2024: 'J135', 2025: 'K135', 2026: 'L135', 2027: 'M135',
            2028: 'N135', 2029: 'O135', 2030: 'P135'
        },
        'Accounts Receivable': {
            2023: 'I136', 2024: 'J136', 2025: 'K136', 2026: 'L136', 2027: 'M136',
            2028: 'N136', 2029: 'O136', 2030: 'P136'
        },
        'Accounts Payable': {
            2023: 'I137', 2024: 'J137', 2025: 'K137', 2026: 'L137', 2027: 'M137',
            2028: 'N137', 2029: 'O137', 2030: 'P137'
        },
        'Other W/C Assets': {
            2023: 'I139', 2024: 'J139', 2025: 'K139', 2026: 'L139', 2027: 'M139',
            2028: 'N139', 2029: 'O139', 2030: 'P139'
        },
        'Other W/C Liabilities': {
            2023: 'I140', 2024: 'J140', 2025: 'K140', 2026: 'L140', 2027: 'M140',
            2028: 'N140', 2029: 'O140', 2030: 'P140'
        },
        'Provisions': {
            2023: 'I142', 2024: 'J142', 2025: 'K142', 2026: 'L142', 2027: 'M142',
            2028: 'N142', 2029: 'O142', 2030: 'P142'
        },
        # Key Stats
        'Revenue growth': {
            2023: 'I145', 2024: 'J145', 2025: 'K145', 2026: 'L145', 2027: 'M145',
            2028: 'N145', 2029: 'O145', 2030: 'P145'
        },
        'EBITDA margin': {
            2023: 'I146', 2024: 'J146', 2025: 'K146', 2026: 'L146', 2027: 'M146',
            2028: 'N146', 2029: 'O146', 2030: 'P146'
        },
        'Depreciation as % of rev.': {
            2023: 'I147', 2024: 'J147', 2025: 'K147', 2026: 'L147', 2027: 'M147',
            2028: 'N147', 2029: 'O147', 2030: 'P147'
        },
        'Amortization as % of rev.': {
            2023: 'I148', 2024: 'J148', 2025: 'K148', 2026: 'L148', 2027: 'M148',
            2028: 'N148', 2029: 'O148', 2030: 'P148'
        },
        'EBIT margin': {
            2023: 'I149', 2024: 'J149', 2025: 'K149', 2026: 'L149', 2027: 'M149',
            2028: 'N149', 2029: 'O149', 2030: 'P149'
        },
        'M-Capex as % of rev.': {
            2023: 'I151', 2024: 'J151', 2025: 'K151', 2026: 'L151', 2027: 'M151',
            2028: 'N151', 2029: 'O151', 2030: 'P151'
        },
        'E-Capex as % of rev.': {
            2023: 'I152', 2024: 'J152', 2025: 'K152', 2026: 'L152', 2027: 'M152',
            2028: 'N152', 2029: 'O152', 2030: 'P152'
        },
        'Inventory as % of rev.': {
            2023: 'I154', 2024: 'J154', 2025: 'K154', 2026: 'L154', 2027: 'M154',
            2028: 'N154', 2029: 'O154', 2030: 'P154'
        },
        'Accounts Receivable as % of rev.': {
            2023: 'I155', 2024: 'J155', 2025: 'K155', 2026: 'L155', 2027: 'M155',
            2028: 'N155', 2029: 'O155', 2030: 'P155'
        },
        'Accounts Payable as % of rev.': {
            2023: 'I156', 2024: 'J156', 2025: 'K156', 2026: 'L156', 2027: 'M156',
            2028: 'N156', 2029: 'O156', 2030: 'P156'
        },
        'Other W/C Assets as % of rev.': {
            2023: 'I124', 2024: 'J124', 2025: 'K124', 2026: 'L124', 2027: 'M124',
            2028: 'N124', 2029: 'O124', 2030: 'P124'
        },
        'Other W/C Liabilities as % of rev.': {
            2023: 'I159', 2024: 'J159', 2025: 'K159', 2026: 'L159', 2027: 'M159',
            2028: 'N159', 2029: 'O159', 2030: 'P159'
        },
        'Provisions growth': {
            2023: 'I161', 2024: 'J161', 2025: 'K161', 2026: 'L161', 2027: 'M161',
            2028: 'N161', 2029: 'O161', 2030: 'P161'
        }
    },
    'Sensitivity Case': {
        # Key P&L Drivers
        'Revenue': {
            2023: 'I173', 2024: 'J173', 2025: 'K173', 2026: 'L173', 2027: 'M173',
            2028: 'N173', 2029: 'O173', 2030: 'P173'
        },
        'EBITDA': {
            2023: 'I174', 2024: 'J174', 2025: 'K174', 2026: 'L174', 2027: 'M174',
            2028: 'N174', 2029: 'O174', 2030: 'P174'
        },
        'EBITDA normalizations': {
            2023: 'I175', 2024: 'J175', 2025: 'K175', 2026: 'L175', 2027: 'M175',
            2028: 'N175', 2029: 'O175', 2030: 'P175'
        },
        'Depreciation': {
            2023: 'I176', 2024: 'J176', 2025: 'K176', 2026: 'L176', 2027: 'M176',
            2028: 'N176', 2029: 'O176', 2030: 'P176'
        },
        'Amortization': {
            2023: 'I177', 2024: 'J177', 2025: 'K177', 2026: 'L177', 2027: 'M177',
            2028: 'N177', 2029: 'O177', 2030: 'P177'
        },
        'EBIT': {
            2023: 'I178', 2024: 'J178', 2025: 'K178', 2026: 'L178', 2027: 'M178',
            2028: 'N178', 2029: 'O178', 2030: 'P178'
        },
        # CapEx
        'Maintenance Capex': {
            2023: 'I181', 2024: 'J181', 2025: 'K181', 2026: 'L181', 2027: 'M181',
            2028: 'N181', 2029: 'O181', 2030: 'P181'
        },
        'Expansion Capex': {
            2023: 'I182', 2024: 'J182', 2025: 'K182', 2026: 'L182', 2027: 'M182',
            2028: 'N182', 2029: 'O182', 2030: 'P182'
        },
        # Balance Sheet Items
        'Inventory': {
            2023: 'I185', 2024: 'J185', 2025: 'K185', 2026: 'L185', 2027: 'M185',
            2028: 'N185', 2029: 'O185', 2030: 'P185'
        },
        'Accounts Receivable': {
            2023: 'I186', 2024: 'J186', 2025: 'K186', 2026: 'L186', 2027: 'M186',
            2028: 'N186', 2029: 'O186', 2030: 'P186'
        },
        'Accounts Payable': {
            2023: 'I187', 2024: 'J187', 2025: 'K187', 2026: 'L187', 2027: 'M187',
            2028: 'N187', 2029: 'O187', 2030: 'P187'
        },
        'Other W/C Assets': {
            2023: 'I189', 2024: 'J189', 2025: 'K189', 2026: 'L189', 2027: 'M189',
            2028: 'N189', 2029: 'O189', 2030: 'P189'
        },
        'Other W/C Liabilities': {
            2023: 'I190', 2024: 'J190', 2025: 'K190', 2026: 'L190', 2027: 'M190',
            2028: 'N190', 2029: 'O190', 2030: 'P190'
        },
        'Provisions': {
            2023: 'I192', 2024: 'J192', 2025: 'K192', 2026: 'L192', 2027: 'M192',
            2028: 'N192', 2029: 'O192', 2030: 'P192'
        },
        # Key Stats
        'Revenue growth': {
            2023: 'I195', 2024: 'J195', 2025: 'K195', 2026: 'L195', 2027: 'M195',
            2028: 'N195', 2029: 'O195', 2030: 'P195'
        },
        'EBITDA margin': {
            2023: 'I196', 2024: 'J196', 2025: 'K196', 2026: 'L196', 2027: 'M196',
            2028: 'N196', 2029: 'O196', 2030: 'P196'
        },
        'Depreciation as % of rev.': {
            2023: 'I197', 2024: 'J197', 2025: 'K197', 2026: 'L197', 2027: 'M197',
            2028: 'N197', 2029: 'O197', 2030: 'P197'
        },
        'Amortization as % of rev.': {
            2023: 'I198', 2024: 'J198', 2025: 'K198', 2026: 'L198', 2027: 'M198',
            2028: 'N198', 2029: 'O198', 2030: 'P198'
        },
        'EBIT margin': {
            2023: 'I199', 2024: 'J199', 2025: 'K199', 2026: 'L199', 2027: 'M199',
            2028: 'N199', 2029: 'O199', 2030: 'P199'
        },
        'M-Capex as % of rev.': {
            2023: 'I201', 2024: 'J201', 2025: 'K201', 2026: 'L201', 2027: 'M201',
            2028: 'N201', 2029: 'O201', 2030: 'P201'
        },
        'E-Capex as % of rev.': {
            2023: 'I202', 2024: 'J202', 2025: 'K202', 2026: 'L202', 2027: 'M202',
            2028: 'N202', 2029: 'O202', 2030: 'P202'
        },
        'Inventory as % of rev.': {
            2023: 'I204', 2024: 'J204', 2025: 'K204', 2026: 'L204', 2027: 'M204',
            2028: 'N204', 2029: 'O204', 2030: 'P204'
        },
        'Accounts Receivable as % of rev.': {
            2023: 'I205', 2024: 'J205', 2025: 'K205', 2026: 'L205', 2027: 'M205',
            2028: 'N205', 2029: 'O205', 2030: 'P205'
        },
        'Accounts Payable as % of rev.': {
            2023: 'I206', 2024: 'J206', 2025: 'K206', 2026: 'L206', 2027: 'M206',
            2028: 'N206', 2029: 'O206', 2030: 'P206'
        },
        'Other W/C Assets as % of rev.': {
            2023: 'I208', 2024: 'J208', 2025: 'K208', 2026: 'L208', 2027: 'M208',
            2028: 'N208', 2029: 'O208', 2030: 'P208'
        },
        'Other W/C Liabilities as % of rev.': {
            2023: 'I209', 2024: 'J209', 2025: 'K209', 2026: 'L209', 2027: 'M209',
            2028: 'N209', 2029: 'O209', 2030: 'P209'
        },
        'Provisions growth': {
            2023: 'I211', 2024: 'J211', 2025: 'K211', 2026: 'L211', 2027: 'M211',
            2028: 'N211', 2029: 'O211', 2030: 'P211'
        }
    },
    'Management Case': {
        # Key P&L Drivers
        'Revenue': {
            2023: 'I73', 2024: 'J73', 2025: 'K73', 2026: 'L73', 2027: 'M73',
            2028: 'N73', 2029: 'O73', 2030: 'P73'
        },
        'EBITDA': {
            2023: 'I74', 2024: 'J74', 2025: 'K74', 2026: 'L74', 2027: 'M74',
            2028: 'N74', 2029: 'O74', 2030: 'P74'
        },
        'EBITDA normalizations': {
            2023: 'I75', 2024: 'J75', 2025: 'K75', 2026: 'L75', 2027: 'M75',
            2028: 'N75', 2029: 'O75', 2030: 'P75'
        },
        'Depreciation': {
            2023: 'I76', 2024: 'J76', 2025: 'K76', 2026: 'L76', 2027: 'M76',
            2028: 'N76', 2029: 'O76', 2030: 'P76'
        },
        'Amortization': {
            2023: 'I77', 2024: 'J77', 2025: 'K77', 2026: 'L77', 2027: 'M77',
            2028: 'N77', 2029: 'O77', 2030: 'P77'
        },
        'EBIT': {
            2023: 'I78', 2024: 'J78', 2025: 'K78', 2026: 'L78', 2027: 'M78',
            2028: 'N78', 2029: 'O78', 2030: 'P78'
        },
        # CapEx
        'Maintenance Capex': {
            2023: 'I81', 2024: 'J81', 2025: 'K81', 2026: 'L81', 2027: 'M81',
            2028: 'N81', 2029: 'O81', 2030: 'P81'
        },
        'Expansion Capex': {
            2023: 'I82', 2024: 'J82', 2025: 'K82', 2026: 'L82', 2027: 'M82',
            2028: 'N82', 2029: 'O82', 2030: 'P82'
        },
        # Balance Sheet Items
        'Inventory': {
            2023: 'I85', 2024: 'J85', 2025: 'K85', 2026: 'L85', 2027: 'M85',
            2028: 'N85', 2029: 'O85', 2030: 'P85'
        },
        'Accounts Receivable': {
            2023: 'I86', 2024: 'J86', 2025: 'K86', 2026: 'L86', 2027: 'M86',
            2028: 'N86', 2029: 'O86', 2030: 'P86'
        },
        'Accounts Payable': {
            2023: 'I87', 2024: 'J87', 2025: 'K87', 2026: 'L87', 2027: 'M87',
            2028: 'N87', 2029: 'O87', 2030: 'P87'
        },
        'Other W/C Assets': {
            2023: 'I89', 2024: 'J89', 2025: 'K89', 2026: 'L89', 2027: 'M89',
            2028: 'N89', 2029: 'O89', 2030: 'P89'
        },
        'Other W/C Liabilities': {
            2023: 'I90', 2024: 'J90', 2025: 'K90', 2026: 'L90', 2027: 'M90',
            2028: 'N90', 2029: 'O90', 2030: 'P90'
        },
        'Provisions': {
            2023: 'I92', 2024: 'J92', 2025: 'K92', 2026: 'L92', 2027: 'M92',
            2028: 'N92', 2029: 'O92', 2030: 'P92'
        },
        # Key Stats
        'Revenue growth': {
            2023: 'I95', 2024: 'J95', 2025: 'K95', 2026: 'L95', 2027: 'M95',
            2028: 'N95', 2029: 'O95', 2030: 'P95'
        },
        'EBITDA margin': {
            2023: 'I96', 2024: 'J96', 2025: 'K96', 2026: 'L96', 2027: 'M96',
            2028: 'N96', 2029: 'O96', 2030: 'P96'
        },
        'Depreciation as % of rev.': {
            2023: 'I97', 2024: 'J97', 2025: 'K97', 2026: 'L97', 2027: 'M97',
            2028: 'N97', 2029: 'O97', 2030: 'P97'
        },
        'Amortization as % of rev.': {
            2023: 'I98', 2024: 'J98', 2025: 'K98', 2026: 'L98', 2027: 'M98',
            2028: 'N98', 2029: 'O98', 2030: 'P98'
        },
        'EBIT margin': {
            2023: 'M99', 2024: 'N99', 2025: 'O99', 2026: 'P99', 2027: 'M99',
            2028: 'N99', 2029: 'O99', 2030: 'P99'
        },
        'M-Capex as % of rev.': {
            2023: 'I101', 2024: 'J101', 2025: 'K101', 2026: 'L101', 2027: 'M101',
            2028: 'N101', 2029: 'O101', 2030: 'P101'
        },
        'E-Capex as % of rev.': {
            2023: 'I102', 2024: 'J102', 2025: 'K102', 2026: 'L102', 2027: 'M102',
            2028: 'N102', 2029: 'O102', 2030: 'P102'
        },
        'Inventory as % of rev.': {
            2023: 'I104', 2024: 'J104', 2025: 'K104', 2026: 'L104', 2027: 'M104',
            2028: 'N104', 2029: 'O104', 2030: 'P104'
        },
        'Accounts Receivable as % of rev.': {
            2023: 'I105', 2024: 'J105', 2025: 'K105', 2026: 'L105', 2027: 'M105',
            2028: 'N105', 2029: 'O105', 2030: 'P105'
        },
        'Accounts Payable as % of rev.': {
            2023: 'I106', 2024: 'J106', 2025: 'K106', 2026: 'L106', 2027: 'M106',
            2028: 'N106', 2029: 'O106', 2030: 'P106'
        },
        'Other W/C Assets as % of rev.': {
            2023: 'I108', 2024: 'J108', 2025: 'K108', 2026: 'L108', 2027: 'M108',
            2028: 'N108', 2029: 'O108', 2030: 'P108'
        },
        'Other W/C Liabilities as % of rev.': {
            2023: 'I109', 2024: 'J109', 2025: 'K109', 2026: 'L109', 2027: 'M109',
            2028: 'N109', 2029: 'O109', 2030: 'P109'
        },
        'Provisions growth': {
            2023: 'I111', 2024: 'J111', 2025: 'K111', 2026: 'L111', 2027: 'M111',
            2028: 'N111', 2029: 'O111', 2030: 'P111'
        }
    },
    'Bottom-Up Case': {
        # Key P&L Drivers
        'Revenue': {
            2023: 'I223', 2024: 'J223', 2025: 'K223', 2026: 'L223', 2027: 'M223',
            2028: 'N223', 2029: 'O223', 2030: 'P223'
        },
        'EBITDA': {
            2023: 'I224', 2024: 'J224', 2025: 'K224', 2026: 'L224', 2027: 'M224',
            2028: 'N224', 2029: 'O224', 2030: 'P224'
        },
        'EBITDA normalizations': {
            2023: 'I225', 2024: 'J225', 2025: 'K225', 2026: 'L225', 2027: 'M225',
            2028: 'N225', 2029: 'O225', 2030: 'P225'
        },
        'Depreciation': {
            2023: 'I226', 2024: 'J226', 2025: 'K226', 2026: 'L226', 2027: 'M226',
            2028: 'N226', 2029: 'O226', 2030: 'P226'
        },
        'Amortization': {
            2023: 'I227', 2024: 'J227', 2025: 'K227', 2026: 'L227', 2027: 'M227',
            2028: 'N227', 2029: 'O227', 2030: 'P227'
        },
        'EBIT': {
            2023: 'I228', 2024: 'J228', 2025: 'K228', 2026: 'L228', 2027: 'M228',
            2028: 'N228', 2029: 'O228', 2030: 'P228'
        },
        # CapEx
        'Maintenance Capex': {
            2023: 'I231', 2024: 'J231', 2025: 'K231', 2026: 'L231', 2027: 'M231',
            2028: 'N231', 2029: 'O231', 2030: 'P231'
        },
        'Expansion Capex': {
            2023: 'I232', 2024: 'J232', 2025: 'K232', 2026: 'L232', 2027: 'M232',
            2028: 'N232', 2029: 'O232', 2030: 'P232'
        },
        # Balance Sheet Items
        'Inventory': {
            2023: 'I235', 2024: 'J235', 2025: 'K235', 2026: 'L235', 2027: 'M235',
            2028: 'N235', 2029: 'O235', 2030: 'P235'
        },
        'Accounts Receivable': {
            2023: 'I236', 2024: 'J236', 2025: 'K236', 2026: 'L236', 2027: 'M236',
            2028: 'N236', 2029: 'O236', 2030: 'P236'
        },
        'Accounts Payable': {
            2023: 'I237', 2024: 'J237', 2025: 'K237', 2026: 'L237', 2027: 'M237',
            2028: 'N237', 2029: 'O237', 2030: 'P237'
        },
        'Other W/C Assets': {
            2023: 'I239', 2024: 'J239', 2025: 'K239', 2026: 'L239', 2027: 'M239',
            2028: 'N239', 2029: 'O239', 2030: 'P239'
        },
        'Other W/C Liabilities': {
            2023: 'I240', 2024: 'J240', 2025: 'K240', 2026: 'L240', 2027: 'M240',
            2028: 'N240', 2029: 'O240', 2030: 'P240'
        },
        'Provisions': {
            2023: 'I242', 2024: 'J242', 2025: 'K242', 2026: 'L242', 2027: 'M242',
            2028: 'N242', 2029: 'O242', 2030: 'P242'
        },
        # Key Stats
        'Revenue growth': {
            2023: 'I245', 2024: 'J245', 2025: 'K245', 2026: 'L245', 2027: 'M245',
            2028: 'N245', 2029: 'O245', 2030: 'P245'
        },
        'EBITDA margin': {
            2023: 'I246', 2024: 'J246', 2025: 'K246', 2026: 'L246', 2027: 'M246',
            2028: 'N246', 2029: 'O246', 2030: 'P246'
        },
        'Depreciation as % of rev.': {
            2023: 'I247', 2024: 'J247', 2025: 'K247', 2026: 'L247', 2027: 'M247',
            2028: 'N247', 2029: 'O247', 2030: 'P247'
        },
        'Amortization as % of rev.': {
            2023: 'I248', 2024: 'J248', 2025: 'K248', 2026: 'L248', 2027: 'M248',
            2028: 'N248', 2029: 'O248', 2030: 'P248'
        },
        'EBIT margin': {
            2023: 'I249', 2024: 'J249', 2025: 'K249', 2026: 'L249', 2027: 'M249',
            2028: 'N249', 2029: 'O249', 2030: 'P249'
        },
        'M-Capex as % of rev.': {
            2023: 'I251', 2024: 'J251', 2025: 'K251', 2026: 'L251', 2027: 'M251',
            2028: 'N251', 2029: 'O251', 2030: 'P251'
        },
        'E-Capex as % of rev.': {
            2023: 'I252', 2024: 'J252', 2025: 'K252', 2026: 'L252', 2027: 'M252',
            2028: 'N252', 2029: 'O252', 2030: 'P252'
        },
        'Inventory as % of rev.': {
            2023: 'I254', 2024: 'J254', 2025: 'K254', 2026: 'L254', 2027: 'M254',
            2028: 'N254', 2029: 'O254', 2030: 'P254'
        },
        'Accounts Receivable as % of rev.': {
            2023: 'I255', 2024: 'J255', 2025: 'K255', 2026: 'L255', 2027: 'M255',
            2028: 'N255', 2029: 'O255', 2030: 'P255'
        },
        'Accounts Payable as % of rev.': {
            2023: 'I256', 2024: 'J256', 2025: 'K256', 2026: 'L256', 2027: 'M256',
            2028: 'N256', 2029: 'O256', 2030: 'P256'
        },
        'Other W/C Assets as % of rev.': {
            2023: 'I258', 2024: 'J258', 2025: 'K258', 2026: 'L258', 2027: 'M258',
            2028: 'N258', 2029: 'O258', 2030: 'P258'
        },
        'Other W/C Liabilities as % of rev.': {
            2023: 'I259', 2024: 'J259', 2025: 'K259', 2026: 'L259', 2027: 'M259',
            2028: 'N259', 2029: 'O259', 2030: 'P259'
        },
        'Provisions growth': {
            2023: 'I261', 2024: 'J261', 2025: 'K261', 2026: 'L261', 2027: 'M261',
            2028: 'N261', 2029: 'O261', 2030: 'P261'
        }
    }
}
