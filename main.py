import os
import sys
from GACPD.GACPD import GACPD

token_list = []
token_file = 'tokens.txt'

if not os.path.exists("reports"):
    os.mkdir("reports")

if not os.path.exists("src"):
    os.mkdir("src")

if not os.path.exists("cmp"):
    os.mkdir("cmp")

print(os.getcwd())

with open(token_file, 'r') as f:
    for line in f.readlines():
        token_list.append(line.strip('\n'))

repos_lastonly = [
    ['ashleyhood/php-lxd', 'turtle0x1/php-lxd'],
    ['kennknowles/python-jsonpath-rw', 'h2non/jsonpath-ng'],
    # ['nathanvda/cocoon', 'notus-sh/cocooned'], # Error with variant not being accessible
    ['nixme/pry-nav', 'garmoshka-mo/pry-moves'],
    ['areski/django-admin-tools-stats', 'PetrDlouhy/django-admin-charts'],
    ['erikrose/blessings', 'jquast/blessed'],
    ['janv/rest_in_place', 'bernat/best_in_place'],
    ['bradleyg/django-s3direct', 'yunojuno/django-s3-upload'],
    ['joshmarshall/jsonrpclib', 'tcalmant/jsonrpclib'],
    ['monitorjbl/excel-streaming-reader', 'pjfanning/excel-streaming-reader'],
    ['FriendsOfSymfony/FOSOAuthServerBundle', 'klapaudius/FOSOAuthServerBundle'],
    ['jcrobak/parquet-python', 'dask/fastparquet'],
    ['Scifabric/pybossa', 'bloomberg/pybossa'],
    ['pdfkit/pdfkit', 'simplybusiness/weasyprint'],
    ['andpor/react-native-sqlite-storage', 'axsy-dev/react-native-sqlcipher-storage'],
    ['arduino/ArduinoCore-samd', 'adafruit/ArduinoCore-samd'],
]

repos_firstonly = [
    ['cardmagic/classifier', 'r00k/simple_classifier'],
    ['carr/phone', 'wmoxam/phonie'],
    ['coleifer/micawber', 'Gurbert/micawber_bs4_classes'],
    ['ethanhann/redisearch-php', 'ashokgit/redisearch-php'],
    ['flori/file-tail', 'octplane/ruby-io-tail'],
    ['heroku/barnes', 'jdejong/takwimu'],
    ['jcrisp/rails_refactor', 'nickdowse/RailsMagicRenamer'],
    ['miguelgrinberg/Flask-HTTPAuth', 'MihaiBalint/Sanic-HTTPAuth'],
    ['spatie/image-optimizer', 'xbing2002/image-optimizer'],
    ['fxn/zeitwerk', 'isomorfeus/opal-zeitwerk'],
    ['github/rubocop-github', 'Springest/rubocop-springest'],
    ['jazzband/django-floppyforms', 'ljean/django-floppyforms'],
    ['jldbc/pybaseball', 'spilchen/baseball_scraper'],
    ['pivotal-energy-solutions/django-datatable-view', 'utapyngo/django-datatable-view'],
    ['unicorn-engine/unicorn', 'yuzu-emu/unicorn'], # yuzu no longer exists
    ['ahupp/python-magic', 'messense/magicfile'],
    ['barryvdh/laravel-translation-manager', 'plus-IT/laravel-translation-manager'],
    ['increments/qiita-rb', 'kachick/qiita-kachick'],
    ['scrapinghub/python-crfsuite', 'bratao/python-crfsuite'],
    ['ethereum/pyrlp', 'Helios-Protocol/py-rlp-cython'],
    ['zopefoundation/zodbpickle', 'moreati/pikl'],
    ['ahupp/python-magic', 'julian-r/python-magic'],
    ['bitcoinj/bitcoinj', 'bisq-network/bitcoinj'],
    ['liuliu/ccv', 'jaysalvat/jquery.facedetection'],
    ['roots/sage', 'itcig/sage-9-timber'],
    ['SciLifeLab/genologics', 'EdinburghGenomics/pyclarity-lims'],
    ['tectonic-typesetting/tectonic', 'crlf0710/tectonic'],
    ['bartTC/dpaste', 'rbarrois/xelpaste'],
    ['Devoxin/Lavalink.py', 'Zenrac/Lavalink.py'],
    ['lorisleiva/laravel-actions', 'larapie/actions'],
    ['petertodd/python-bitcoinlib', 'Simplexum/python-bitcointx'],
    ['lbeder/health-monitor-rails', 'rails-engine/status-page'],
    ['anexia-it/django-rest-passwordreset', 'alonraiz/django-rest-passwordreset'],
    ['manodeep/Corrfunc', 'kstoreyf/suave'],
    ['posativ/isso', 'staugur/isso-cn'],
    ['Tautulli/Tautulli', 'zSeriesGuy/Tautulli'],
    ['amoffat/sh', 'xapple/pbs3'],
    ['pry/pry-doc', 'janlelis/core_docs'],
    ['Alir3z4/html2text', 'Pavkazzz/html2texttg'],
    ['onelogin/php-saml', 'workivate/php-saml'],
    ['jstasiak/python-zeroconf', 'learningequality/python-zeroconf-py2compat'],
    ['adamchainz/django-cors-headers', 'zestedesavoir/django-cors-middleware'],
    ['korfuri/django-prometheus', 'prezi/django-exporter'],
    ['MichaelGrupp/evo', 'ToniRV/evo-1'],
    ['rgeo/activerecord-postgis-adapter', 'teeparham/ar-postgis'],
    ['KnpLabs/DictionaryBundle', 'biig-io/DictionaryBundle'],
    ['guard/listen', 'sass/listen'],
    ['coleifer/peewee', '311devs/peewee'],
    ['jstasiak/python-zeroconf', 'frawau/aiozeroconf'],
    ['spatie/ssl-certificate', 'liquidweb/ssl-certificate'],
    ['gleitz/howdoi', 'chrisspen/howdou'],
    ['PyMySQL/PyMySQL', 'python-trio/trio-mysql'],
    ['lark-parser/lark', 'evandrocoan/pushdown'],
    # ['Slimefun/Slimefun4', 'StarWishsama/Slimefun4'], # issues with repo
    ['datastax/python-driver', 'YugaByte/cassandra-python-driver'],
    ['posativ/isso', 'pellenilsson/isso'],
    ['spesmilo/electrum', 'namecoin/electrum-nmc'],
    ['mmistakes/minimal-mistakes', 'bwiedermann/benimal-mistakes'],
    ['nerdvegas/rez', 'mottosso/bleeding-rez'],
    ['cloudtools/troposphere', 'QualiNext/ionosphere'],
    ['libffi/libffi', 'frida/libffi'],
    ['OctoPrint/OctoPrint', 'beeverycreative/BEEweb'],
    ['spesmilo/electrum', 'wo01/electrum-koto'],
    ['puppetlabs/showoff', 'burtlo/parade'],
    ['uken/fluent-plugin-elasticsearch', 'haruyama/fluent-plugin-out-solr'],
    ['jazzband/pip-tools', 'jgonggrijp/pip-review'],
    ['DSpace/DSpace', 'datadryad/dryad-repo'],
    ['vector-im/riot-android', 'LiMium/mini-vector-android'],
    ['stellar/stellar-core', 'buhrmi/open-core'],
    ['qmk/qmk_firmware', 'sekigon-gonnoc/qmk_firmware'],
    ['cupy/cupy', 'fixstars/clpy'],
]

repos_both = [
    ['dlindahl/omniauth-cas', 'tduehr/omniauth-cas3'],
    ['ekohl/metadata_json_deps', 'puppetlabs/dependency_checker'],
    ['lemurheavy/coveralls-ruby', 'tagliala/coveralls-ruby-reborn'],
    ['openssh/openssh-portable', 'PowerShell/openssh-portable'],
    # ['openssl/openssl', 'open-quantum-safe/openssl'], # not checked - too big
    ['cweiske/jsonmapper', 'apimatic/jsonmapper'],
    ['paramiko/paramiko', 'ploxiln/paramiko-ng'],
    ['jagrosh/MusicBot', 'Cosgy-Dev/JMusicBot-JP'],
    ['bitcoinj/bitcoinj', 'langerhans/dogecoinj-new'],
    ['micke/valid_email2', 'wolfemm/email_assessor'],
    ['NickWaterton/Roomba980-Python', 'pschmitt/roombapy'],
    ['jekyll/jekyll-admin', 'ashmaroli/jekyll-manager'],
    ['ledermann/rails-settings', 'huacnlee/rails-settings-cached'],
    ['getredash/redash', 'mozilla/redash'],
    ['DMTF/python-redfish-library', 'HewlettPackard/python-ilorest-library'],
    ['coderholic/django-cities', 'yourlabs/django-cities-light'],
    ['spesmilo/electrum', 'Electron-Cash/Electron-Cash'],
    ['apache/roller', 'gmazza/tightblog'],
    ['google/styleguide', 'cpplint/cpplint'],
    ['datastax/python-driver', 'scylladb/python-driver'],
    ['javacc/javacc', 'phax/ParserGeneratorCC'],
    ['NCAR/ParallelIO', 'E3SM-Project/scorpio'],
    ['python-pillow/Pillow', 'uploadcare/pillow-simd'],
    # ['curl/curl', 'Unity-Technologies/curl'], Too big to check
    # ['prestodb/presto', 'twitter-forks/presto'], Too big to check
    ['xerial/sqlite-jdbc', 'Willena/sqlite-jdbc-crypt'],
    ['apache/mynewt-nimble', 'espressif/esp-nimble'],
    ['easybuilders/easybuild-easyconfigs', 'ComputeCanada/easybuild-easyconfigs'],
    ['spesmilo/electrum', 'exoeconomy/EXOS-Electrum'],
    ['spesmilo/electrum', 'Groestlcoin/electrum-grs'],
    # ['PyMySQL/PyMySQL', 'nakagami/CyMySQL'], # not checked - too big
    # ['DMOJ/online-judge', 'mcpt/wlmoj'], # not checked - too big
    # ['DSpace/DSpace', 'ufal/clarin-dspace'], # not checked - too big
    # ['DataDog/dd-trace-rb', 'lightstep/ls-trace-rb'], # not checked - too big
    # ['edx/configuration', 'appsembler/configuration'], # not checked - too big
    # ['collectd/collectd', 'Stackdriver/collectd'], # not checked - too big
    # ['qmk/qmk_firmware', 'zsa/qmk_firmware'], # not checked - too big
    # ['microsoft/azure-tools-for-java', 'JetBrains/azure-tools-for-intellij'], # not checked - too big
    # ['qmk/qmk_firmware', 'germ/qmk_firmware'], # not checked - too big
    # ['spack/spack', 'BlueBrain/spack'], # not checked - too big
    # ['apache/kafka', 'linkedin/kafka'], # not checked - too big
]

i = 0
j = 0
k = 0
z = 0

for k in range(0, len(repos_lastonly)):
    data = (str(i), repos_lastonly[k][1], repos_lastonly[k][0], token_list, '', '')
    example = GACPD(data)
    example.get_dates()
    prs_source = example.extractPatches(example.get_cretion_date(repos_lastonly[k][0]), example.divergence_date)
    example.dfPatches()
    example.runClassification(prs_source)
    i = i+1

for j in range(0, len(repos_firstonly)):
    data = (str(i), repos_firstonly[j][0], repos_firstonly[j][1], token_list, '', '')
    example = GACPD(data)
    example.get_dates()
    prs_source = example.extractPatches(example.get_cretion_date(repos_firstonly[j][0]), example.divergence_date)
    example.dfPatches()
    example.runClassification(prs_source)
    i = i + 1

for z in range(0, len(repos_both)):
    data = (str(i), repos_both[z][0], repos_both[z][1], token_list, '', '')
    example = GACPD(data)
    example.get_dates()
    prs_source = example.extractPatches(example.get_cretion_date(repos_both[z][0]), example.divergence_date)
    example.dfPatches()
    example.runClassification(prs_source)

    i = i+1
    data = (str(i), repos_both[z][1], repos_both[z][0], token_list, '', '')
    example = GACPD(data)
    example.get_dates()
    prs_source = example.extractPatches(example.get_cretion_date(repos_both[z][1]), example.divergence_date)
    example.dfPatches()
    example.runClassification(prs_source)
    i = i + 1

example.create_dynamic_js()