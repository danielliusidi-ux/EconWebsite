from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, gettext as _
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

# 配置Babel
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
babel = Babel(app)

# 简单的翻译函数，直接从.po文件中读取翻译
_translations = {}
_translation_stamp = None

# 加载翻译
import os
import re

def load_translations():
    global _translations
    _translations = {}
    # 使用绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(base_dir, 'translations')
    
    if not os.path.exists(translations_dir):
        return
    
    for lang in os.listdir(translations_dir):
        if lang.startswith('.'): continue
        
        lang_dir = os.path.join(translations_dir, lang, 'LC_MESSAGES')
        po_file = os.path.join(lang_dir, 'messages.po')
        
        if os.path.exists(po_file):
            _translations[lang] = {}
            
            with open(po_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                current_msgid = None
                current_msgstr = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('msgid "') and line.endswith('"'):
                        current_msgid = line[7:-1]
                    elif line.startswith('msgstr "') and line.endswith('"'):
                        current_msgstr = line[8:-1]
                        if current_msgid:
                            _translations[lang][current_msgid] = current_msgstr
                            current_msgid = None


def _compute_translation_stamp():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(base_dir, 'translations')
    stamp = []
    if not os.path.exists(translations_dir):
        return tuple(stamp)
    for lang in sorted(os.listdir(translations_dir)):
        if lang.startswith('.'):
            continue
        po_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
        if os.path.exists(po_file):
            try:
                stamp.append((lang, os.path.getmtime(po_file)))
            except OSError:
                stamp.append((lang, None))
    return tuple(stamp)


def refresh_translations_if_needed():
    global _translation_stamp
    stamp = _compute_translation_stamp()
    if stamp != _translation_stamp:
        _translation_stamp = stamp
        load_translations()

# 加载翻译
load_translations()

# 覆盖gettext函数
from flask_babel import gettext as original_gettext
def gettext(message):
    refresh_translations_if_needed()
    lang = get_locale()
    # print(f"Translating '{message}' to {lang}")
    if lang in _translations and message in _translations[lang]:
        # print(f"Found translation for '{message}': {_translations[lang][message]}")
        return _translations[lang][message]
    return message

# 替换Flask-Babel的gettext
import builtins
builtins._ = gettext

# 将自定义gettext注入到Jinja2环境
app.jinja_env.globals.update(_=gettext)
app.jinja_env.globals.update(gettext=gettext)

# 语言配置
LANGUAGES = {
    'en': 'English',
    'zh': '中文'
}

# 获取用户语言偏好
@babel.localeselector
def get_locale():
    if 'language' in session:
        return session['language']
    return 'en'  # 默认语言为英语

# 切换语言
@app.route('/change-language/<lang>')
def change_language(lang):
    if lang in LANGUAGES:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

# 模拟题库数据（实际应用中应使用数据库）
QUESTION_BANK = {
    'ap_micro': [
        {
            'id': 1,
            'question': 'Which of the following is a characteristic of a perfectly competitive market?',
            'options': ['A) Firms are price makers', 'B) There are barriers to entry', 'C) Firms produce homogeneous products', 'D) There are few sellers'],
            'answer': 'C',
            'explanation': 'In a perfectly competitive market, firms produce homogeneous (identical) products, there are no barriers to entry, firms are price takers, and there are many sellers.',
            'topic': 'Market Structures'
        },
        {
            'id': 2,
            'question': 'What is the formula for calculating marginal cost?',
            'options': ['A) Change in total cost divided by change in quantity', 'B) Total cost divided by quantity', 'C) Change in total variable cost divided by change in quantity', 'D) Both A and C'],
            'answer': 'D',
            'explanation': 'Marginal cost can be calculated as either the change in total cost divided by the change in quantity or the change in total variable cost divided by the change in quantity, since fixed costs do not change with quantity.',
            'topic': 'Costs of Production'
        },
        {
            'id': 3,
            'question': 'If the price of a good increases by 10% and the quantity demanded decreases by 20%, what is the price elasticity of demand?',
            'options': ['A) 0.5', 'B) 2.0', 'C) 10.0', 'D) 20.0'],
            'answer': 'B',
            'explanation': 'Price elasticity of demand = (% Change in Quantity Demanded) / (% Change in Price) = 20% / 10% = 2.0. The demand is elastic.',
            'topic': 'Elasticity'
        },
        {
            'id': 4,
            'question': 'Consumer surplus is defined as the difference between:',
            'options': ['A) The price consumers are willing to pay and the price they actually pay', 'B) The price producers are willing to sell for and the price they actually receive', 'C) Total revenue and total cost', 'D) The maximum price and the minimum price'],
            'answer': 'A',
            'explanation': 'Consumer surplus is the difference between the maximum price a consumer is willing to pay and the actual market price they pay.',
            'topic': 'Consumer Surplus'
        },
        {
            'id': 5,
            'question': 'In a monopoly, the firm maximizes profit by producing the quantity where:',
            'options': ['A) Price equals marginal cost (P = MC)', 'B) Marginal revenue equals marginal cost (MR = MC)', 'C) Average total cost is minimized', 'D) Marginal cost equals average total cost (MC = ATC)'],
            'answer': 'B',
            'explanation': 'A monopoly (like other firms) maximizes profit at the quantity where marginal revenue equals marginal cost (MR = MC). It then charges the highest price consumers will pay for that quantity on the demand curve.',
            'topic': 'Market Structures'
        },
        {
            'id': 6,
            'question': 'Which market structure is characterized by differentiated products and many sellers?',
            'options': ['A) Perfect competition', 'B) Monopoly', 'C) Monopolistic competition', 'D) Oligopoly'],
            'answer': 'C',
            'explanation': 'Monopolistic competition has many sellers and product differentiation. Firms have some price-setting power but face competition from close substitutes.',
            'topic': 'Market Structures'
        },
        {
            'id': 7,
            'question': 'A price floor set above the equilibrium price will most likely result in:',
            'options': ['A) A shortage', 'B) A surplus', 'C) No change in quantity traded', 'D) Higher equilibrium quantity'],
            'answer': 'B',
            'explanation': 'A binding price floor is set above equilibrium. Quantity supplied exceeds quantity demanded, creating a surplus.',
            'topic': 'Market Intervention'
        },
        {
            'id': 8,
            'question': 'If demand is inelastic, a decrease in price will:',
            'options': ['A) Increase total revenue', 'B) Decrease total revenue', 'C) Leave total revenue unchanged', 'D) Make demand more elastic'],
            'answer': 'B',
            'explanation': 'With inelastic demand, quantity changes proportionally less than price. Lower price reduces total revenue (P×Q).',
            'topic': 'Elasticity'
        },
        {
            'id': 9,
            'question': 'Producer surplus is best described as:',
            'options': ['A) The difference between the market price and the minimum price producers are willing to accept', 'B) The difference between the maximum price consumers will pay and the market price', 'C) Total revenue minus total cost', 'D) A tax collected by the government'],
            'answer': 'A',
            'explanation': 'Producer surplus is the difference between the market price received and the minimum price producers would accept for each unit.',
            'topic': 'Producer Surplus'
        },
        {
            'id': 10,
            'question': 'A negative externality in production causes the market equilibrium quantity to be:',
            'options': ['A) Lower than the socially optimal quantity', 'B) Higher than the socially optimal quantity', 'C) Equal to the socially optimal quantity', 'D) Zero'],
            'answer': 'B',
            'explanation': 'With a negative production externality, social cost exceeds private cost, so the market produces too much relative to the socially efficient outcome.',
            'topic': 'Externalities'
        },
        {
            'id': 11,
            'question': 'If the government imposes a per-unit tax on buyers, the demand curve will:',
            'options': ['A) Shift right', 'B) Shift left', 'C) Rotate clockwise', 'D) Not change'],
            'answer': 'B',
            'explanation': 'A tax on buyers increases the effective price paid, reducing quantity demanded at each market price; this is represented as a leftward shift of demand.',
            'topic': 'Market Intervention'
        },
        {
            'id': 12,
            'question': 'Deadweight loss from a tax is:',
            'options': ['A) The tax revenue collected', 'B) The loss of total surplus from reduced trade', 'C) The increase in producer surplus', 'D) The area under the demand curve'],
            'answer': 'B',
            'explanation': 'A tax reduces the quantity traded below the efficient level, causing a loss in total surplus that is not captured as tax revenue.',
            'topic': 'Market Intervention'
        },
        {
            'id': 13,
            'question': 'When marginal product of labor is diminishing, marginal cost will generally:',
            'options': ['A) Fall', 'B) Rise', 'C) Stay constant', 'D) Become zero'],
            'answer': 'B',
            'explanation': 'With diminishing marginal product, each additional unit of output requires more labor, raising the cost of producing an extra unit (MC rises).',
            'topic': 'Costs of Production'
        },
        {
            'id': 14,
            'question': 'Average variable cost (AVC) is calculated as:',
            'options': ['A) Total cost / quantity', 'B) Fixed cost / quantity', 'C) Variable cost / quantity', 'D) Total revenue / quantity'],
            'answer': 'C',
            'explanation': 'AVC is variable cost per unit of output: AVC = TVC / Q.',
            'topic': 'Costs of Production'
        },
        {
            'id': 15,
            'question': 'A firm in a perfectly competitive market earns economic profit in the short run when:',
            'options': ['A) P < AVC', 'B) P = ATC', 'C) P > ATC', 'D) P = MC always'],
            'answer': 'C',
            'explanation': 'Economic profit occurs when price exceeds average total cost at the profit-maximizing output (where P = MR = MC).',
            'topic': 'Perfect Competition'
        },
        {
            'id': 16,
            'question': 'In the long run under perfect competition, firms earn:',
            'options': ['A) Positive economic profit', 'B) Zero economic profit', 'C) Negative economic profit always', 'D) Monopoly profit'],
            'answer': 'B',
            'explanation': 'Free entry and exit drive long-run economic profit to zero (P = min ATC).',
            'topic': 'Perfect Competition'
        },
        {
            'id': 17,
            'question': 'If a firm experiences decreasing returns to scale, then when all inputs are increased by 10%, output will:',
            'options': ['A) Increase by more than 10%', 'B) Increase by exactly 10%', 'C) Increase by less than 10%', 'D) Fall by 10%'],
            'answer': 'C',
            'explanation': 'Decreasing returns to scale means output increases by a smaller percentage than inputs.',
            'topic': 'Production'
        },
        {
            'id': 18,
            'question': 'A firm should shut down in the short run if:',
            'options': ['A) P < AVC', 'B) P < ATC but P > AVC', 'C) P = MC', 'D) P > ATC'],
            'answer': 'A',
            'explanation': 'If price is below average variable cost, the firm cannot cover variable costs and should shut down in the short run.',
            'topic': 'Costs of Production'
        },
        {
            'id': 19,
            'question': 'In an oligopoly, firms are said to be interdependent because:',
            'options': ['A) Each firm ignores rivals\' actions', 'B) Each firm\'s actions affect rivals\' profits', 'C) Products are always identical', 'D) There are no barriers to entry'],
            'answer': 'B',
            'explanation': 'Oligopoly features a small number of firms; pricing/output decisions affect competitors, so firms must consider rivals\' responses.',
            'topic': 'Market Structures'
        },
        {
            'id': 20,
            'question': 'Price discrimination is most likely to be successful when:',
            'options': ['A) Consumers can easily resell the product', 'B) Demand elasticities differ across groups', 'C) The firm is a price taker', 'D) There are many identical sellers'],
            'answer': 'B',
            'explanation': 'A monopolist can increase profit by charging different prices to groups with different price elasticities, provided resale is limited.',
            'topic': 'Market Structures'
        },
        {
            'id': 21,
            'question': 'If the cross-price elasticity of demand between two goods is positive, the goods are:',
            'options': ['A) Complements', 'B) Substitutes', 'C) Inferior goods', 'D) Unrelated'],
            'answer': 'B',
            'explanation': 'A positive cross-price elasticity indicates the goods are substitutes: when price of one rises, demand for the other increases.',
            'topic': 'Elasticity'
        },
        {
            'id': 22,
            'question': 'If a good has income elasticity of demand less than 0, it is:',
            'options': ['A) A normal good', 'B) An inferior good', 'C) A luxury good', 'D) A public good'],
            'answer': 'B',
            'explanation': 'Negative income elasticity indicates demand falls when income rises, which defines an inferior good.',
            'topic': 'Elasticity'
        },
        {
            'id': 23,
            'question': 'A binding price ceiling will usually cause:',
            'options': ['A) A surplus', 'B) A shortage', 'C) A higher equilibrium price', 'D) No change in quantity traded'],
            'answer': 'B',
            'explanation': 'A binding price ceiling is below equilibrium, increasing quantity demanded and decreasing quantity supplied, creating a shortage.',
            'topic': 'Market Intervention'
        },
        {
            'id': 24,
            'question': 'If a firm is operating where marginal cost is below average total cost, then average total cost will:',
            'options': ['A) Rise', 'B) Fall', 'C) Stay constant', 'D) Become negative'],
            'answer': 'B',
            'explanation': 'When MC < ATC, producing one more unit pulls the average down, so ATC decreases.',
            'topic': 'Costs of Production'
        },
        {
            'id': 25,
            'question': 'If marginal revenue is greater than marginal cost at the current output, a profit-maximizing firm should:',
            'options': ['A) Decrease output', 'B) Increase output', 'C) Keep output unchanged', 'D) Shut down immediately'],
            'answer': 'B',
            'explanation': 'If MR > MC, producing additional units increases profit; the firm should increase output until MR = MC.',
            'topic': 'Profit Maximization'
        }
    ],
    'ap_macro': [
        {
            'id': 1,
            'question': 'Which of the following is included in the calculation of GDP using the expenditure approach?',
            'options': ['A) Transfer payments', 'B) Intermediate goods', 'C) Government spending on public goods', 'D) Financial investments'],
            'answer': 'C',
            'explanation': 'The expenditure approach to GDP includes consumption, investment, government spending, and net exports. Government spending on public goods is included, while transfer payments, intermediate goods, and financial investments are not.',
            'topic': 'GDP Calculation'
        },
        {
            'id': 2,
            'question': 'Who is most likely to be hurt by unanticipated inflation?',
            'options': ['A) Borrowers with fixed-rate loans', 'B) Lenders with fixed-rate loans', 'C) Producers selling goods at flexible prices', 'D) Workers with cost-of-living adjustments'],
            'answer': 'B',
            'explanation': 'Unanticipated inflation reduces the real value of money paid back to lenders. Borrowers benefit because they pay back loans with less valuable dollars. Lenders are hurt.',
            'topic': 'Inflation'
        },
        {
            'id': 3,
            'question': 'Which of the following is an expansionary monetary policy?',
            'options': ['A) Increasing the reserve requirement', 'B) Increasing the discount rate', 'C) Buying government bonds', 'D) Increasing taxes'],
            'answer': 'C',
            'explanation': 'Buying government bonds increases the money supply, lowers interest rates, and stimulates the economy, making it an expansionary monetary policy.',
            'topic': 'Monetary Policy'
        },
        {
            'id': 4,
            'question': 'If the unemployment rate is above the natural rate, which fiscal policy is most appropriate?',
            'options': ['A) Decrease government spending', 'B) Increase taxes', 'C) Increase government spending', 'D) Decrease the money supply'],
            'answer': 'C',
            'explanation': 'High cyclical unemployment suggests recessionary conditions. Expansionary fiscal policy (increase G or decrease T) raises aggregate demand and employment.',
            'topic': 'Fiscal Policy'
        },
        {
            'id': 5,
            'question': 'A higher price level, holding everything else constant, will typically:',
            'options': ['A) Increase aggregate demand', 'B) Decrease aggregate demand', 'C) Increase short-run aggregate supply', 'D) Decrease long-run aggregate supply'],
            'answer': 'B',
            'explanation': 'A higher price level reduces real balances and purchasing power, leading to lower consumption and net exports; this is a movement along the AD curve.',
            'topic': 'Aggregate Demand'
        },
        {
            'id': 6,
            'question': 'When the central bank increases the reserve requirement, the money multiplier will:',
            'options': ['A) Increase', 'B) Decrease', 'C) Stay the same', 'D) Become negative'],
            'answer': 'B',
            'explanation': 'A higher reserve requirement reduces the fraction of deposits banks can lend, lowering the money multiplier.',
            'topic': 'Money Multiplier'
        },
        {
            'id': 7,
            'question': 'Cost-push inflation is most likely caused by:',
            'options': ['A) An increase in aggregate demand', 'B) A decrease in short-run aggregate supply', 'C) An increase in long-run aggregate supply', 'D) A decrease in the price level'],
            'answer': 'B',
            'explanation': 'Cost-push inflation results from rising production costs that shift SRAS left, increasing the price level and reducing output in the short run.',
            'topic': 'Inflation'
        },
        {
            'id': 8,
            'question': 'An increase in the value of a country\'s currency will generally make its exports:',
            'options': ['A) Cheaper for foreigners', 'B) More expensive for foreigners', 'C) Unaffected in price', 'D) Illegal to purchase'],
            'answer': 'B',
            'explanation': 'Appreciation makes domestic goods more expensive to foreign buyers, tending to reduce exports and increase imports.',
            'topic': 'Exchange Rates'
        },
        {
            'id': 9,
            'question': 'If real GDP is increasing while the price level is decreasing, which shift is most consistent with this outcome?',
            'options': ['A) AD shifts left', 'B) SRAS shifts right', 'C) SRAS shifts left', 'D) AD shifts right and SRAS shifts left'],
            'answer': 'B',
            'explanation': 'A rightward shift of SRAS increases output and lowers the price level.',
            'topic': 'AD-AS'
        },
        {
            'id': 10,
            'question': 'The natural rate of unemployment includes:',
            'options': ['A) Cyclical unemployment only', 'B) Frictional and structural unemployment', 'C) Structural unemployment only', 'D) All unemployment including cyclical'],
            'answer': 'B',
            'explanation': 'The natural rate consists of frictional and structural unemployment; cyclical unemployment is excluded.',
            'topic': 'Unemployment'
        },
        {
            'id': 11,
            'question': 'If nominal GDP rises while real GDP is unchanged, it is likely that:',
            'options': ['A) The price level increased', 'B) Output increased', 'C) Unemployment fell', 'D) Productivity fell'],
            'answer': 'A',
            'explanation': 'Nominal GDP changes reflect both price and output. If real GDP is unchanged, the rise in nominal GDP is due to higher prices.',
            'topic': 'GDP Calculation'
        },
        {
            'id': 12,
            'question': 'Crowding out refers to:',
            'options': ['A) Tax cuts increasing investment', 'B) Government borrowing raising interest rates and reducing private investment', 'C) Monetary expansion reducing output', 'D) Imports reducing exports'],
            'answer': 'B',
            'explanation': 'Expansionary fiscal policy can raise interest rates via borrowing, which may reduce private investment spending.',
            'topic': 'Fiscal Policy'
        },
        {
            'id': 13,
            'question': 'If a country runs a persistent current account deficit, it is likely that:',
            'options': ['A) Exports exceed imports', 'B) Imports exceed exports', 'C) The currency is pegged to gold', 'D) Government spending is zero'],
            'answer': 'B',
            'explanation': 'A current account deficit generally means net exports are negative: imports exceed exports.',
            'topic': 'International Trade'
        },
        {
            'id': 14,
            'question': 'An increase in productivity is most likely to shift:',
            'options': ['A) SRAS left', 'B) SRAS right', 'C) AD left', 'D) AD right only'],
            'answer': 'B',
            'explanation': 'Higher productivity lowers unit costs and increases capacity, shifting SRAS to the right.',
            'topic': 'Aggregate Supply'
        },
        {
            'id': 15,
            'question': 'The Phillips curve in the short run suggests a trade-off between:',
            'options': ['A) Inflation and unemployment', 'B) GDP and interest rates', 'C) Exports and imports', 'D) Taxes and spending'],
            'answer': 'A',
            'explanation': 'In the short run, lower unemployment is associated with higher inflation and vice versa, though this trade-off can break down.',
            'topic': 'Phillips Curve'
        },
        {
            'id': 16,
            'question': 'If the central bank sells government securities on the open market, the money supply will:',
            'options': ['A) Increase', 'B) Decrease', 'C) Stay the same', 'D) Become infinite'],
            'answer': 'B',
            'explanation': 'Selling bonds pulls reserves from the banking system, decreasing the money supply and raising interest rates.',
            'topic': 'Monetary Policy'
        },
        {
            'id': 17,
            'question': 'If inflation is lower than expected, who benefits?',
            'options': ['A) Borrowers with fixed-rate loans', 'B) Lenders with fixed-rate loans', 'C) Firms with flexible prices', 'D) Governments that print money'],
            'answer': 'B',
            'explanation': 'Lower-than-expected inflation increases the real value of repayments, benefiting lenders and hurting borrowers.',
            'topic': 'Inflation'
        },
        {
            'id': 18,
            'question': 'Real interest rate is approximately equal to:',
            'options': ['A) Nominal interest rate + inflation', 'B) Nominal interest rate − inflation', 'C) Inflation − nominal interest rate', 'D) Nominal GDP − real GDP'],
            'answer': 'B',
            'explanation': 'Real interest rate ≈ nominal interest rate minus inflation.',
            'topic': 'Interest Rates'
        },
        {
            'id': 19,
            'question': 'A decrease in taxes, holding government spending constant, will tend to:',
            'options': ['A) Decrease aggregate demand', 'B) Increase aggregate demand', 'C) Shift SRAS left', 'D) Increase the natural rate of unemployment'],
            'answer': 'B',
            'explanation': 'Lower taxes increase disposable income and consumption, raising aggregate demand (expansionary fiscal policy).',
            'topic': 'Fiscal Policy'
        },
        {
            'id': 20,
            'question': 'If wages are sticky downward, a decrease in aggregate demand is more likely to lead to:',
            'options': ['A) Immediate full employment at a lower wage', 'B) A short-run fall in output and rise in unemployment', 'C) A long-run rise in output', 'D) No change in unemployment'],
            'answer': 'B',
            'explanation': 'Sticky wages slow adjustment, so AD decreases reduce output in the short run, raising cyclical unemployment.',
            'topic': 'AD-AS'
        },
        {
            'id': 21,
            'question': 'The GDP deflator is used to:',
            'options': ['A) Measure unemployment', 'B) Convert nominal GDP to real GDP', 'C) Measure trade deficits', 'D) Calculate tax revenue'],
            'answer': 'B',
            'explanation': 'Real GDP = Nominal GDP / (GDP deflator/100). The deflator adjusts for price level changes.',
            'topic': 'GDP Calculation'
        },
        {
            'id': 22,
            'question': 'Stagflation refers to:',
            'options': ['A) Falling prices and rising output', 'B) Rising prices and falling output', 'C) Rising output and stable prices', 'D) Falling unemployment and falling inflation'],
            'answer': 'B',
            'explanation': 'Stagflation is a combination of high inflation and low growth (often with rising unemployment), commonly from a negative supply shock.',
            'topic': 'Inflation'
        },
        {
            'id': 23,
            'question': 'If a country\'s currency depreciates, net exports will most likely:',
            'options': ['A) Decrease because exports become more expensive', 'B) Increase because exports become cheaper for foreigners', 'C) Remain unchanged always', 'D) Become negative by definition'],
            'answer': 'B',
            'explanation': 'Depreciation makes exports cheaper and imports more expensive, tending to increase net exports (depending on elasticities).',
            'topic': 'Exchange Rates'
        },
        {
            'id': 24,
            'question': 'Which of the following best describes automatic stabilizers?',
            'options': ['A) Policies that require new legislation each recession', 'B) Features like taxes and unemployment benefits that dampen fluctuations', 'C) Central bank open market operations', 'D) Price controls to stabilize inflation'],
            'answer': 'B',
            'explanation': 'Automatic stabilizers change government spending or tax revenue automatically as income changes, reducing volatility without new policy decisions.',
            'topic': 'Fiscal Policy'
        },
        {
            'id': 25,
            'question': 'If expected inflation rises, nominal interest rates will tend to:',
            'options': ['A) Fall', 'B) Rise', 'C) Stay constant', 'D) Become negative'],
            'answer': 'B',
            'explanation': 'By the Fisher effect, higher expected inflation leads lenders to demand higher nominal interest rates.',
            'topic': 'Interest Rates'
        }
    ],
    'igcse': [
        {
            'id': 1,
            'question': 'What is the basic economic problem?',
            'options': ['A) Scarcity', 'B) Inflation', 'C) Unemployment', 'D) Economic growth'],
            'answer': 'A',
            'explanation': 'The basic economic problem is scarcity, which arises because resources are limited but wants are unlimited.',
            'topic': 'Basic Economic Concepts'
        },
        {
            'id': 2,
            'question': 'Which factor of production includes tools, machinery, and buildings?',
            'options': ['A) Land', 'B) Labor', 'C) Capital', 'D) Enterprise'],
            'answer': 'C',
            'explanation': 'Capital refers to man-made resources used in production, such as tools, machinery, equipment, and buildings.',
            'topic': 'Factors of Production'
        },
        {
            'id': 3,
            'question': 'According to the law of demand, when the price of a good increases, ceteris paribus:',
            'options': ['A) Demand increases', 'B) Quantity demanded decreases', 'C) Supply increases', 'D) Quantity supplied decreases'],
            'answer': 'B',
            'explanation': 'The law of demand states that there is an inverse relationship between price and quantity demanded. As price rises, quantity demanded falls.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 4,
            'question': 'A production possibility curve (PPC) illustrates:',
            'options': ['A) Unlimited resources and wants', 'B) The trade-off between producing two goods', 'C) The relationship between price and quantity demanded', 'D) The number of firms in a market'],
            'answer': 'B',
            'explanation': 'A PPC shows the maximum combinations of two goods that can be produced given current resources and technology, highlighting opportunity cost.',
            'topic': 'Basic Economic Concepts'
        },
        {
            'id': 5,
            'question': 'Which of the following is most likely to cause a decrease in demand for a normal good?',
            'options': ['A) An increase in consumer income', 'B) A decrease in consumer income', 'C) A fall in the price of the good', 'D) A rise in the price of a substitute'],
            'answer': 'B',
            'explanation': 'For a normal good, demand moves in the same direction as income. Lower income reduces demand.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 6,
            'question': 'Price elasticity of demand measures:',
            'options': ['A) The responsiveness of quantity demanded to a change in price', 'B) The responsiveness of supply to a change in income', 'C) The responsiveness of price to a change in quantity demanded', 'D) The responsiveness of demand to a change in population'],
            'answer': 'A',
            'explanation': 'PED measures how much quantity demanded changes when price changes, ceteris paribus.',
            'topic': 'Elasticity'
        },
        {
            'id': 7,
            'question': 'A subsidy given to producers will most likely:',
            'options': ['A) Decrease supply', 'B) Increase supply', 'C) Decrease demand', 'D) Increase demand'],
            'answer': 'B',
            'explanation': 'A subsidy lowers production costs, shifting the supply curve to the right (increase supply).',
            'topic': 'Government Intervention'
        },
        {
            'id': 8,
            'question': 'A public good is typically:',
            'options': ['A) Rival and excludable', 'B) Non-rival and non-excludable', 'C) Rival and non-excludable', 'D) Non-rival and excludable'],
            'answer': 'B',
            'explanation': 'Public goods are non-rival (one person\'s use doesn\'t reduce availability) and non-excludable (difficult to prevent non-payers from consuming).',
            'topic': 'Market Failure'
        },
        {
            'id': 9,
            'question': 'Opportunity cost is best defined as:',
            'options': ['A) The total monetary cost of production', 'B) The value of the next best alternative forgone', 'C) The value of all alternatives', 'D) The profit earned from a decision'],
            'answer': 'B',
            'explanation': 'Opportunity cost is what you give up when choosing one option over the next best alternative.',
            'topic': 'Basic Economic Concepts'
        },
        {
            'id': 10,
            'question': 'If supply increases and demand is unchanged, equilibrium price will:',
            'options': ['A) Rise', 'B) Fall', 'C) Stay the same', 'D) Become negative'],
            'answer': 'B',
            'explanation': 'An increase in supply shifts the supply curve right, lowering the equilibrium price and increasing equilibrium quantity.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 11,
            'question': 'A maximum price (price ceiling) set below equilibrium will usually lead to:',
            'options': ['A) Surplus', 'B) Shortage', 'C) Higher equilibrium price', 'D) No change in quantity'],
            'answer': 'B',
            'explanation': 'A binding price ceiling increases quantity demanded and decreases quantity supplied, creating a shortage.',
            'topic': 'Government Intervention'
        },
        {
            'id': 12,
            'question': 'Division of labour can increase productivity because it:',
            'options': ['A) Eliminates scarcity', 'B) Allows workers to specialize and become more efficient', 'C) Raises all wages immediately', 'D) Removes the need for capital'],
            'answer': 'B',
            'explanation': 'Specialization improves skill, reduces switching time, and can encourage use of machinery, raising productivity.',
            'topic': 'Production'
        },
        {
            'id': 13,
            'question': 'Which is most likely an example of a fixed cost?',
            'options': ['A) Raw materials', 'B) Hourly wages of temporary workers', 'C) Monthly rent of a factory', 'D) Electricity for machines'],
            'answer': 'C',
            'explanation': 'Fixed costs do not vary with output in the short run; rent is typically fixed.',
            'topic': 'Costs of Production'
        },
        {
            'id': 14,
            'question': 'A fall in the price of a complement will likely:',
            'options': ['A) Decrease demand for the good', 'B) Increase demand for the good', 'C) Decrease supply of the good', 'D) Increase price elasticity always'],
            'answer': 'B',
            'explanation': 'Complements are used together; a cheaper complement increases demand for the related good.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 15,
            'question': 'If demand is price elastic, a rise in price will tend to:',
            'options': ['A) Increase total revenue', 'B) Decrease total revenue', 'C) Leave total revenue unchanged', 'D) Increase quantity demanded'],
            'answer': 'B',
            'explanation': 'With elastic demand, quantity falls proportionally more than price rises, so total revenue decreases.',
            'topic': 'Elasticity'
        },
        {
            'id': 16,
            'question': 'Which of the following is a possible disadvantage of specialization?',
            'options': ['A) Lower output', 'B) Greater boredom and repetitive work', 'C) Elimination of trade', 'D) Lower efficiency'],
            'answer': 'B',
            'explanation': 'Specialization can lead to repetitive tasks and lower job satisfaction, even though it often increases productivity.',
            'topic': 'Production'
        },
        {
            'id': 17,
            'question': 'A regressive tax is one where the tax as a percentage of income:',
            'options': ['A) Rises as income rises', 'B) Falls as income rises', 'C) Stays constant for all incomes', 'D) Is unrelated to income'],
            'answer': 'B',
            'explanation': 'Regressive taxes take a larger percentage of income from low-income earners than from high-income earners.',
            'topic': 'Government Intervention'
        },
        {
            'id': 18,
            'question': 'An indirect tax (like a sales tax) imposed on producers will most likely:',
            'options': ['A) Shift supply left', 'B) Shift supply right', 'C) Shift demand right', 'D) Shift demand left only'],
            'answer': 'A',
            'explanation': 'An indirect tax increases production costs, shifting supply left, raising price and lowering quantity.',
            'topic': 'Government Intervention'
        },
        {
            'id': 19,
            'question': 'Inflation refers to:',
            'options': ['A) A fall in the general price level', 'B) A sustained rise in the general price level', 'C) A rise in output only', 'D) A fall in unemployment'],
            'answer': 'B',
            'explanation': 'Inflation is a sustained increase in the general price level over time.',
            'topic': 'Macroeconomics'
        },
        {
            'id': 20,
            'question': 'Economic growth is commonly measured by:',
            'options': ['A) Inflation rate', 'B) Real GDP growth', 'C) Nominal wage growth', 'D) Stock prices'],
            'answer': 'B',
            'explanation': 'Economic growth refers to increases in real output, often measured by real GDP growth.',
            'topic': 'Macroeconomics'
        },
        {
            'id': 21,
            'question': 'A decrease in unemployment benefits may (all else equal):',
            'options': ['A) Increase frictional unemployment', 'B) Reduce frictional unemployment', 'C) Increase inflation always', 'D) Eliminate structural unemployment'],
            'answer': 'B',
            'explanation': 'Lower benefits can reduce the time people spend searching, potentially lowering frictional unemployment (though with trade-offs).',
            'topic': 'Unemployment'
        },
        {
            'id': 22,
            'question': 'A monopoly differs from perfect competition mainly because a monopoly:',
            'options': ['A) Is a price taker', 'B) Faces a downward-sloping demand curve', 'C) Produces homogeneous products only', 'D) Has no barriers to entry'],
            'answer': 'B',
            'explanation': 'A monopoly is a price maker and faces the market demand curve, which is downward sloping.',
            'topic': 'Market Structures'
        },
        {
            'id': 23,
            'question': 'A rise in the price of a substitute good will likely:',
            'options': ['A) Decrease demand for the good', 'B) Increase demand for the good', 'C) Decrease supply of the good', 'D) Decrease equilibrium price always'],
            'answer': 'B',
            'explanation': 'If a substitute becomes more expensive, consumers switch to the other good, increasing its demand.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 24,
            'question': 'A market failure occurs when:',
            'options': ['A) Markets always clear', 'B) Markets allocate resources inefficiently', 'C) Firms earn profits', 'D) Consumers have choices'],
            'answer': 'B',
            'explanation': 'Market failure is when the market outcome is not allocatively efficient, often due to externalities, public goods, or market power.',
            'topic': 'Market Failure'
        },
        {
            'id': 25,
            'question': 'A positive externality results in a market equilibrium quantity that is:',
            'options': ['A) Too high', 'B) Too low', 'C) Efficient', 'D) Zero'],
            'answer': 'B',
            'explanation': 'With positive externalities, social benefits exceed private benefits, so the market under-produces relative to the social optimum.',
            'topic': 'Market Failure'
        }
    ],
    'a_level': [
        {
            'id': 1,
            'question': 'Which of the following is a merit good?',
            'options': ['A) Tobacco', 'B) Education', 'C) Alcohol', 'D) Junk food'],
            'answer': 'B',
            'explanation': 'A merit good is a good that is underprovided by the market because its benefits are not fully recognized by consumers. Education is a merit good because it provides positive externalities to society.',
            'topic': 'Market Failure'
        },
        {
            'id': 2,
            'question': 'Which component is the largest part of Aggregate Demand in most economies?',
            'options': ['A) Investment', 'B) Government Spending', 'C) Consumption', 'D) Net Exports'],
            'answer': 'C',
            'explanation': 'Consumption (household spending) is typically the largest component of Aggregate Demand in most economies.',
            'topic': 'Aggregate Demand'
        },
        {
            'id': 3,
            'question': 'A depreciation of a country\'s currency is likely to lead to:',
            'options': ['A) Cheaper imports and more expensive exports', 'B) More expensive imports and cheaper exports', 'C) No change in trade balance', 'D) Lower inflation'],
            'answer': 'B',
            'explanation': 'Depreciation makes a country\'s currency weaker. This makes imports more expensive (need more domestic currency to buy foreign goods) and exports cheaper for foreigners.',
            'topic': 'Exchange Rates'
        },
        {
            'id': 4,
            'question': 'A negative externality in consumption leads to:',
            'options': ['A) Under-consumption relative to the social optimum', 'B) Over-consumption relative to the social optimum', 'C) No inefficiency because markets always clear', 'D) Higher consumer surplus without any cost'],
            'answer': 'B',
            'explanation': 'When consumption imposes external costs (e.g., second-hand smoke), the market outcome has too much consumption compared with the socially efficient level.',
            'topic': 'Market Failure'
        },
        {
            'id': 5,
            'question': 'In the AD-AS model, a rightward shift of short-run aggregate supply (SRAS) will typically:',
            'options': ['A) Increase the price level and decrease real output', 'B) Decrease the price level and increase real output', 'C) Increase both price level and output', 'D) Decrease both price level and output'],
            'answer': 'B',
            'explanation': 'A rightward shift of SRAS represents lower costs or higher productivity, increasing output while reducing the price level in the short run.',
            'topic': 'Aggregate Supply'
        },
        {
            'id': 6,
            'question': 'Which of the following is a typical objective of government macroeconomic policy?',
            'options': ['A) Perfect equality of income', 'B) Full employment', 'C) Eliminating all imports', 'D) Zero economic growth'],
            'answer': 'B',
            'explanation': 'Common objectives include full employment, stable prices, sustainable growth, and a stable balance of payments.',
            'topic': 'Macroeconomic Objectives'
        },
        {
            'id': 7,
            'question': 'A firm in an oligopoly may avoid lowering prices because:',
            'options': ['A) It faces no competition', 'B) It expects rivals to match price cuts, reducing gains', 'C) Demand is perfectly inelastic', 'D) Marginal cost is always zero'],
            'answer': 'B',
            'explanation': 'In oligopoly, interdependence matters. Price cuts are often matched, leading to little increase in market share but lower profits for all firms.',
            'topic': 'Market Structures'
        },
        {
            'id': 8,
            'question': 'If demand for a product increases while supply remains constant, equilibrium price and quantity will:',
            'options': ['A) Both fall', 'B) Both rise', 'C) Price rises and quantity falls', 'D) Price falls and quantity rises'],
            'answer': 'B',
            'explanation': 'An increase in demand shifts the demand curve right, raising both equilibrium price and equilibrium quantity.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 9,
            'question': 'A demerit good is one that:',
            'options': ['A) Generates positive external benefits', 'B) Is over-consumed due to information failure', 'C) Is always under-supplied by markets', 'D) Has perfectly elastic demand'],
            'answer': 'B',
            'explanation': 'Demerit goods (e.g., cigarettes) may be over-consumed because consumers underestimate true costs; they often create negative externalities.',
            'topic': 'Market Failure'
        },
        {
            'id': 10,
            'question': 'A specific (per-unit) tax on producers will most likely:',
            'options': ['A) Shift supply left', 'B) Shift supply right', 'C) Shift demand right', 'D) Increase quantity traded'],
            'answer': 'A',
            'explanation': 'A per-unit tax increases firms\' marginal costs, shifting supply left; price rises and quantity falls.',
            'topic': 'Government Intervention'
        },
        {
            'id': 11,
            'question': 'In the long run, if firms are making supernormal profit in monopolistic competition, we expect:',
            'options': ['A) Firms to exit, shifting demand right', 'B) New firms to enter, shifting demand left for each firm', 'C) No entry due to barriers', 'D) Prices to be fixed by government'],
            'answer': 'B',
            'explanation': 'Free entry reduces each firm\'s demand as more substitutes appear; long-run economic profit tends toward zero.',
            'topic': 'Market Structures'
        },
        {
            'id': 12,
            'question': 'A subsidy to producers will tend to:',
            'options': ['A) Raise price and lower quantity', 'B) Lower price and raise quantity', 'C) Raise both price and quantity', 'D) Lower both price and quantity'],
            'answer': 'B',
            'explanation': 'A subsidy lowers costs, shifting supply right; equilibrium price falls and quantity rises.',
            'topic': 'Government Intervention'
        },
        {
            'id': 13,
            'question': 'Price discrimination requires that a firm can:',
            'options': ['A) Prevent resale between consumers', 'B) Be a price taker', 'C) Have zero fixed costs', 'D) Face perfectly elastic demand'],
            'answer': 'A',
            'explanation': 'To price discriminate, the firm must segment markets and prevent arbitrage (resale) between groups.',
            'topic': 'Market Structures'
        },
        {
            'id': 14,
            'question': 'In the AD-AS framework, a decrease in aggregate demand will most likely cause:',
            'options': ['A) Higher price level and higher output', 'B) Lower price level and lower output in the short run', 'C) Higher price level and lower output', 'D) No change in unemployment'],
            'answer': 'B',
            'explanation': 'A leftward shift of AD reduces output and the price level in the short run.',
            'topic': 'Aggregate Demand'
        },
        {
            'id': 15,
            'question': 'A positive externality in production means that:',
            'options': ['A) Private cost exceeds social cost', 'B) Social cost exceeds private cost', 'C) Social benefit exceeds private benefit', 'D) Private benefit exceeds social benefit'],
            'answer': 'C',
            'explanation': 'With positive externalities, third parties gain benefits not reflected in the market price; MSB > MPB.',
            'topic': 'Market Failure'
        },
        {
            'id': 16,
            'question': 'Which policy is most directly aimed at reducing negative externalities?',
            'options': ['A) Subsidies to consumers', 'B) Indirect taxes on the activity', 'C) Price ceilings', 'D) Increasing advertising'],
            'answer': 'B',
            'explanation': 'Taxes can internalize external costs by raising the private cost closer to the social cost.',
            'topic': 'Government Intervention'
        },
        {
            'id': 17,
            'question': 'A current account deficit implies that a country is:',
            'options': ['A) Exporting more than importing', 'B) Importing more than exporting', 'C) Running a budget surplus', 'D) Experiencing deflation'],
            'answer': 'B',
            'explanation': 'A current account deficit corresponds to negative net exports: imports exceed exports.',
            'topic': 'International Trade'
        },
        {
            'id': 18,
            'question': 'When a currency appreciates, we would generally expect:',
            'options': ['A) Exports to rise and imports to fall', 'B) Exports to fall and imports to rise', 'C) Both exports and imports to rise', 'D) No impact on trade'],
            'answer': 'B',
            'explanation': 'Appreciation makes exports more expensive and imports cheaper, reducing exports and increasing imports.',
            'topic': 'Exchange Rates'
        },
        {
            'id': 19,
            'question': 'If marginal cost is below average variable cost, then average variable cost will:',
            'options': ['A) Rise', 'B) Fall', 'C) Stay constant', 'D) Equal marginal cost'],
            'answer': 'B',
            'explanation': 'When MC < AVC, producing one more unit pulls the average down, so AVC decreases.',
            'topic': 'Costs of Production'
        },
        {
            'id': 20,
            'question': 'The main purpose of competition policy (antitrust) is to:',
            'options': ['A) Increase unemployment', 'B) Promote competitive markets and prevent abuse of market power', 'C) Eliminate all profits', 'D) Set all prices by law'],
            'answer': 'B',
            'explanation': 'Competition policy aims to maintain competition, reduce monopoly power, and improve allocative efficiency.',
            'topic': 'Market Structures'
        },
        {
            'id': 21,
            'question': 'A fall in interest rates is most likely to:',
            'options': ['A) Decrease investment', 'B) Increase investment', 'C) Shift AD left', 'D) Reduce consumption always'],
            'answer': 'B',
            'explanation': 'Lower interest rates reduce the cost of borrowing, typically encouraging investment and some consumption, raising AD.',
            'topic': 'Macroeconomic Objectives'
        },
        {
            'id': 22,
            'question': 'If the government sets a minimum wage above equilibrium, the most likely outcome is:',
            'options': ['A) Labor shortage', 'B) Labor surplus (unemployment)', 'C) No change in employment', 'D) Higher equilibrium wage'],
            'answer': 'B',
            'explanation': 'A binding wage floor raises the wage, increasing labor supply and reducing labor demand, creating unemployment.',
            'topic': 'Government Intervention'
        },
        {
            'id': 23,
            'question': 'In perfect competition, allocative efficiency occurs where:',
            'options': ['A) P > MC', 'B) P = MC', 'C) MR = 0', 'D) ATC is maximized'],
            'answer': 'B',
            'explanation': 'Allocative efficiency occurs when price equals marginal cost, so the value to consumers equals the cost of producing the last unit.',
            'topic': 'Perfect Competition'
        },
        {
            'id': 24,
            'question': 'A key assumption of the circular flow model is that:',
            'options': ['A) There is no government', 'B) Resources are unlimited', 'C) All markets are perfectly competitive', 'D) Households own factors of production'],
            'answer': 'D',
            'explanation': 'In the basic circular flow, households own factors (labor, land, capital, enterprise) and sell them to firms.',
            'topic': 'Basic Economic Concepts'
        },
        {
            'id': 25,
            'question': 'If an economy is operating inside its PPC, it indicates:',
            'options': ['A) Full employment and efficiency', 'B) Underutilization of resources', 'C) Technological progress', 'D) Impossible combinations'],
            'answer': 'B',
            'explanation': 'Points inside the PPC indicate unemployed or inefficiently used resources; the economy could produce more of both goods.',
            'topic': 'Basic Economic Concepts'
        }
    ],
    'dse': [
        {
            'id': 1,
            'question': 'What is the opportunity cost of a decision?',
            'options': ['A) The total cost of the decision', 'B) The monetary cost of the decision', 'C) The value of the next best alternative foregone', 'D) The benefits of the decision'],
            'answer': 'C',
            'explanation': 'Opportunity cost is the value of the next best alternative that is given up when making a decision.',
            'topic': 'Basic Economic Concepts'
        },
        {
            'id': 2,
            'question': 'Which of the following is a result of an effective price ceiling?',
            'options': ['A) Surplus', 'B) Shortage', 'C) Equilibrium', 'D) Higher quality goods'],
            'answer': 'B',
            'explanation': 'An effective price ceiling is set below the equilibrium price. At this lower price, quantity demanded exceeds quantity supplied, creating a shortage.',
            'topic': 'Market Intervention'
        },
        {
            'id': 3,
            'question': 'Comparative advantage is based on:',
            'options': ['A) Absolute cost', 'B) Opportunity cost', 'C) Labor cost', 'D) Transportation cost'],
            'answer': 'B',
            'explanation': 'Comparative advantage is the ability to produce a good at a lower opportunity cost than another producer. It is the basis for trade.',
            'topic': 'International Trade'
        },
        {
            'id': 4,
            'question': 'If the price of a normal good rises, the quantity demanded will generally:',
            'options': ['A) Increase', 'B) Decrease', 'C) Stay the same', 'D) Become zero'],
            'answer': 'B',
            'explanation': 'By the law of demand, higher price leads to lower quantity demanded, ceteris paribus.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 5,
            'question': 'A per-unit tax imposed on sellers will most likely:',
            'options': ['A) Shift supply left (decrease supply)', 'B) Shift demand right (increase demand)', 'C) Increase consumer surplus', 'D) Eliminate scarcity'],
            'answer': 'A',
            'explanation': 'A tax increases sellers\' costs, shifting the supply curve left. Equilibrium price rises and quantity falls.',
            'topic': 'Government Intervention'
        },
        {
            'id': 6,
            'question': 'Which of the following is an example of a positive externality?',
            'options': ['A) Pollution from a factory', 'B) Noise from construction', 'C) Vaccination reducing the spread of disease', 'D) Traffic congestion'],
            'answer': 'C',
            'explanation': 'Vaccination generates benefits to third parties by reducing transmission, a positive externality.',
            'topic': 'Externalities'
        },
        {
            'id': 7,
            'question': 'A merit good is one that:',
            'options': ['A) Is over-consumed because it is addictive', 'B) Is under-consumed because people underestimate its benefits', 'C) Has no external benefits', 'D) Is always provided efficiently by markets'],
            'answer': 'B',
            'explanation': 'Merit goods (e.g., education) are under-consumed if individuals undervalue their private and social benefits.',
            'topic': 'Market Failure'
        },
        {
            'id': 8,
            'question': 'Under free trade, countries specialize according to comparative advantage because it can:',
            'options': ['A) Reduce total world output', 'B) Increase total world output', 'C) Guarantee equal incomes', 'D) Eliminate opportunity cost'],
            'answer': 'B',
            'explanation': 'Specialization based on comparative advantage raises total output and allows mutually beneficial trade.',
            'topic': 'International Trade'
        },
        {
            'id': 9,
            'question': 'If the price of a good rises and quantity demanded falls, this is best described as:',
            'options': ['A) A shift in demand', 'B) A movement along the demand curve', 'C) A shift in supply', 'D) A change in preferences only'],
            'answer': 'B',
            'explanation': 'A price change causes a movement along the existing demand curve; shifts come from non-price determinants.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 10,
            'question': 'An increase in the number of sellers in a market will likely:',
            'options': ['A) Decrease supply', 'B) Increase supply', 'C) Decrease demand', 'D) Increase demand'],
            'answer': 'B',
            'explanation': 'More sellers increase the market supply at each price, shifting supply to the right.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 11,
            'question': 'A shortage occurs when:',
            'options': ['A) Quantity supplied exceeds quantity demanded', 'B) Quantity demanded exceeds quantity supplied', 'C) The market is at equilibrium', 'D) Price is above equilibrium'],
            'answer': 'B',
            'explanation': 'At the given price, if quantity demanded is greater than quantity supplied, there is a shortage.',
            'topic': 'Supply and Demand'
        },
        {
            'id': 12,
            'question': 'Which of the following would shift demand for a good to the right?',
            'options': ['A) A fall in income for a normal good', 'B) A rise in the price of a substitute', 'C) A fall in the price of the good itself', 'D) An increase in supply'],
            'answer': 'B',
            'explanation': 'If substitutes become more expensive, consumers switch to this good, increasing its demand (shift right).',
            'topic': 'Supply and Demand'
        },
        {
            'id': 13,
            'question': 'An indirect tax on a good is most likely to:',
            'options': ['A) Lower the market price and raise quantity', 'B) Raise the market price and lower quantity', 'C) Raise both price and quantity', 'D) Have no effect on equilibrium'],
            'answer': 'B',
            'explanation': 'A tax shifts supply left, raising price paid by consumers and reducing equilibrium quantity.',
            'topic': 'Government Intervention'
        },
        {
            'id': 14,
            'question': 'A subsidy to producers will most likely:',
            'options': ['A) Reduce supply', 'B) Increase supply', 'C) Reduce demand', 'D) Eliminate opportunity cost'],
            'answer': 'B',
            'explanation': 'A subsidy lowers production costs and shifts supply right, increasing quantity and lowering price.',
            'topic': 'Government Intervention'
        },
        {
            'id': 15,
            'question': 'A negative externality in consumption leads to:',
            'options': ['A) Over-consumption relative to the social optimum', 'B) Under-consumption relative to the social optimum', 'C) No inefficiency', 'D) Zero consumption'],
            'answer': 'A',
            'explanation': 'If consumers ignore external costs, they consume more than is socially efficient (MSB < MPB is false; rather MSC > MPC or MSB? here external costs).',
            'topic': 'Externalities'
        },
        {
            'id': 16,
            'question': 'A public good is characterized by being:',
            'options': ['A) Rival and excludable', 'B) Non-rival and non-excludable', 'C) Rival and non-excludable', 'D) Non-rival and excludable'],
            'answer': 'B',
            'explanation': 'Public goods are non-rival and non-excludable, which can lead to free-rider problems.',
            'topic': 'Market Failure'
        },
        {
            'id': 17,
            'question': 'Which policy is most suitable for correcting a negative externality?',
            'options': ['A) Subsidy', 'B) Per-unit tax', 'C) Price ceiling', 'D) Import tariff'],
            'answer': 'B',
            'explanation': 'A tax can internalize external costs, reducing the activity toward the socially optimal level.',
            'topic': 'Government Intervention'
        },
        {
            'id': 18,
            'question': 'Economic efficiency in consumption occurs when:',
            'options': ['A) Price equals marginal cost', 'B) Marginal benefit equals marginal cost', 'C) Total revenue equals total cost', 'D) Demand is perfectly inelastic'],
            'answer': 'B',
            'explanation': 'Allocative efficiency occurs when MB = MC, ensuring resources are allocated to their highest-valued use.',
            'topic': 'Basic Economic Concepts'
        },
        {
            'id': 19,
            'question': 'If a country has a comparative advantage in a good, it means:',
            'options': ['A) It can produce it with fewer resources in absolute terms', 'B) It has a lower opportunity cost of producing it', 'C) It always exports all goods', 'D) It has higher wages'],
            'answer': 'B',
            'explanation': 'Comparative advantage is determined by opportunity cost, not absolute cost.',
            'topic': 'International Trade'
        },
        {
            'id': 20,
            'question': 'A tariff is:',
            'options': ['A) A tax on exports', 'B) A tax on imports', 'C) A subsidy to consumers', 'D) A price ceiling'],
            'answer': 'B',
            'explanation': 'A tariff is a tax on imported goods, making them more expensive and protecting domestic producers.',
            'topic': 'International Trade'
        },
        {
            'id': 21,
            'question': 'The main aim of protectionism is to:',
            'options': ['A) Increase consumer choice at lower prices', 'B) Protect domestic industries from foreign competition', 'C) Eliminate all trade', 'D) Reduce productivity'],
            'answer': 'B',
            'explanation': 'Protectionist measures like tariffs and quotas are intended to shield domestic producers.',
            'topic': 'International Trade'
        },
        {
            'id': 22,
            'question': 'Inflation reduces purchasing power because:',
            'options': ['A) Money becomes more valuable', 'B) The general price level rises', 'C) Output always falls', 'D) Taxes always fall'],
            'answer': 'B',
            'explanation': 'When prices rise, each unit of currency buys fewer goods and services, reducing purchasing power.',
            'topic': 'Macroeconomics'
        },
        {
            'id': 23,
            'question': 'Unemployment refers to people who are:',
            'options': ['A) Not working and not looking for work', 'B) Working part-time voluntarily', 'C) Not working but actively seeking work', 'D) Under 16 years old'],
            'answer': 'C',
            'explanation': 'The unemployed are those without a job who are available and actively searching for work.',
            'topic': 'Unemployment'
        },
        {
            'id': 24,
            'question': 'Economic growth can be driven by:',
            'options': ['A) A fall in productivity', 'B) Technological progress and investment', 'C) A reduction in education', 'D) Higher unemployment'],
            'answer': 'B',
            'explanation': 'Investment, better education, and technology improve productivity and expand productive capacity, supporting growth.',
            'topic': 'Macroeconomics'
        },
        {
            'id': 25,
            'question': 'A trade-off shown by a PPC illustrates:',
            'options': ['A) Unlimited resources', 'B) Opportunity cost', 'C) Money illusion', 'D) Perfect information'],
            'answer': 'B',
            'explanation': 'Moving along the PPC requires giving up some of one good to produce more of another, reflecting opportunity cost.',
            'topic': 'Basic Economic Concepts'
        }
    ]
}


def ensure_question_difficulties():
    def infer_difficulty(question_id):
        if not isinstance(question_id, int):
            return 'Medium'
        if question_id <= 8:
            return 'Easy'
        if question_id <= 17:
            return 'Medium'
        return 'Hard'

    for exam_type, questions in QUESTION_BANK.items():
        for q in questions:
            if 'difficulty' not in q or not q.get('difficulty'):
                q['difficulty'] = infer_difficulty(q.get('id'))


ensure_question_difficulties()



from flask import jsonify

# 模拟用户进度数据 (在实际应用中应存储在数据库中)
# 结构: exam_type -> {completed: set(question_ids), correct: set(question_ids), total_attempts: 0}
USER_PROGRESS = {
    'ap_micro': {'completed': set(), 'correct': set(), 'total_attempts': 0},
    'ap_macro': {'completed': set(), 'correct': set(), 'total_attempts': 0},
    'igcse': {'completed': set(), 'correct': set(), 'total_attempts': 0},
    'a_level': {'completed': set(), 'correct': set(), 'total_attempts': 0},
    'dse': {'completed': set(), 'correct': set(), 'total_attempts': 0}
}

# 辅助函数：获取用户统计
def get_user_stats():
    total_completed = 0
    total_correct = 0
    
    stats = {}
    
    for exam_type, data in USER_PROGRESS.items():
        completed_count = len(data['completed'])
        correct_count = len(data['correct'])
        accuracy = int((correct_count / completed_count * 100)) if completed_count > 0 else 0
        questions = QUESTION_BANK.get(exam_type, [])
        total_questions = len(questions)

        difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0}
        for q in questions:
            diff = (q.get('difficulty') or 'Medium').strip().lower()
            if diff not in difficulty_counts:
                diff = 'medium'
            difficulty_counts[diff] += 1

        if total_questions > 0:
            difficulty_percent = {
                k: int(round(v / total_questions * 100))
                for k, v in difficulty_counts.items()
            }
        else:
            difficulty_percent = {'easy': 0, 'medium': 0, 'hard': 0}
        
        stats[exam_type] = {
            'completed': completed_count,
            'accuracy': accuracy,
            'total_questions': total_questions,
            'difficulty_counts': difficulty_counts,
            'difficulty_percent': difficulty_percent
        }
        
        total_completed += completed_count
        total_correct += correct_count
        
    total_accuracy = int((total_correct / total_completed * 100)) if total_completed > 0 else 0
    
    return {
        'total_practiced': total_completed,
        'today_completed': total_completed, # 暂用总数代替
        'today_accuracy': total_accuracy,
        'exam_stats': stats
    }


def infer_exam_type_for_question(question):
    question_id = question.get('id')
    question_text = question.get('question')
    question_topic = question.get('topic')

    for exam_type, questions in QUESTION_BANK.items():
        for q in questions:
            if q.get('id') == question_id and q.get('question') == question_text and q.get('topic') == question_topic:
                return exam_type
    return None


# 首页
@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES, current_language=get_locale())

# 选择考试类型
@app.route('/select-exam')
def select_exam():
    stats = get_user_stats()
    return render_template('select_exam.html', 
                           languages=LANGUAGES, 
                           current_language=get_locale(),
                           stats=stats)

# 刷题页面 (单题模式)
@app.route('/practice/<exam_type>')
@app.route('/practice/<exam_type>/<int:question_index>')
def practice(exam_type, question_index=0):
    if exam_type not in QUESTION_BANK:
        return redirect(url_for('select_exam'))
    
    difficulty = request.args.get('difficulty')
    difficulty = difficulty.strip().lower() if isinstance(difficulty, str) else None
    difficulty_map = {'easy': 'Easy', 'medium': 'Medium', 'hard': 'Hard'}
    difficulty_label = difficulty_map.get(difficulty)

    questions_all = QUESTION_BANK[exam_type]
    if difficulty_label:
        questions = [q for q in questions_all if (q.get('difficulty') or 'Medium') == difficulty_label]
    else:
        questions = questions_all

    if not questions:
        return redirect(url_for('practice', exam_type=exam_type))

    total_questions = len(questions)
    
    # 确保索引有效
    if question_index >= total_questions:
        return redirect(url_for('select_exam'))
        
    current_question = questions[question_index]
    
    # 获取当前进度
    progress = USER_PROGRESS.get(exam_type, {'completed': set(), 'correct': set()})
    completed_count = len(progress['completed'])
    accuracy = 0
    if completed_count > 0:
        accuracy = int(len(progress['correct']) / completed_count * 100)
        
    next_url = None
    finish_url = url_for('select_exam')
    if question_index + 1 < total_questions:
        if difficulty_label:
            next_url = url_for('practice', exam_type=exam_type, question_index=question_index + 1, difficulty=difficulty_label)
        else:
            next_url = url_for('practice', exam_type=exam_type, question_index=question_index + 1)

    return render_template('practice.html', 
                           exam_type=exam_type,
                           question=current_question,
                           question_index=question_index,
                           total_questions=total_questions,
                           completed_count=completed_count,
                           accuracy=accuracy,
                           back_url=url_for('select_exam'),
                           next_url=next_url,
                           finish_url=finish_url,
                           difficulty_filter=difficulty_label,
                           languages=LANGUAGES, 
                           current_language=get_locale())


@app.route('/practice-similar/<exam_type>/<path:topic>')
@app.route('/practice-similar/<exam_type>/<path:topic>/<int:question_index>')
def practice_similar(exam_type, topic, question_index=0):
    if exam_type not in QUESTION_BANK:
        return redirect(url_for('wrong_questions'))

    exclude_id = request.args.get('exclude_id', type=int)
    difficulty = request.args.get('difficulty')
    difficulty = difficulty.strip().lower() if isinstance(difficulty, str) else None
    difficulty_map = {'easy': 'Easy', 'medium': 'Medium', 'hard': 'Hard'}
    difficulty_label = difficulty_map.get(difficulty)
    all_questions = QUESTION_BANK[exam_type]
    filtered = [q for q in all_questions if q.get('topic') == topic and (exclude_id is None or q.get('id') != exclude_id)]
    if difficulty_label:
        filtered = [q for q in filtered if (q.get('difficulty') or 'Medium') == difficulty_label]

    total_questions = len(filtered)
    if total_questions == 0:
        return redirect(url_for('wrong_questions'))

    if question_index >= total_questions:
        return redirect(url_for('wrong_questions'))

    current_question = filtered[question_index]

    progress = USER_PROGRESS.get(exam_type, {'completed': set(), 'correct': set()})
    completed_count = len(progress['completed'])
    accuracy = 0
    if completed_count > 0:
        accuracy = int(len(progress['correct']) / completed_count * 100)

    next_url = None
    finish_url = url_for('wrong_questions')
    if question_index + 1 < total_questions:
        if difficulty_label:
            next_url = url_for('practice_similar', exam_type=exam_type, topic=topic, question_index=question_index + 1, exclude_id=exclude_id, difficulty=difficulty_label)
        else:
            next_url = url_for('practice_similar', exam_type=exam_type, topic=topic, question_index=question_index + 1, exclude_id=exclude_id)

    return render_template('practice.html',
                           exam_type=exam_type,
                           question=current_question,
                           question_index=question_index,
                           total_questions=total_questions,
                           completed_count=completed_count,
                           accuracy=accuracy,
                           back_url=url_for('wrong_questions'),
                           next_url=next_url,
                           finish_url=finish_url,
                           difficulty_filter=difficulty_label,
                           languages=LANGUAGES,
                           current_language=get_locale())

# 提交答案 API
@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    data = request.json
    exam_type = data.get('exam_type')
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    
    if exam_type not in QUESTION_BANK:
        return jsonify({'error': 'Invalid exam type'}), 400
        
    questions = QUESTION_BANK[exam_type]
    question = next((q for q in questions if q['id'] == question_id), None)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
        
    is_correct = (user_answer == question['answer'])
    
    # 更新统计
    if exam_type in USER_PROGRESS:
        USER_PROGRESS[exam_type]['completed'].add(question_id)
        USER_PROGRESS[exam_type]['total_attempts'] += 1
        if is_correct:
            USER_PROGRESS[exam_type]['correct'].add(question_id)
        else:
            # 记录错题到 session
            if 'wrong_questions' not in session:
                session['wrong_questions'] = []
            # 避免重复添加
            wrong_item = dict(question)
            wrong_item['exam_type'] = exam_type
            if not any(q.get('id') == question.get('id') and q.get('exam_type') == exam_type for q in session['wrong_questions']):
                session['wrong_questions'].append(wrong_item)
                session.modified = True
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': question['answer'],
        'explanation': question['explanation']
    })

# 错题本
@app.route('/wrong-questions')
def wrong_questions():
    wrong_questions = session.get('wrong_questions', [])
    enriched = []
    for q in wrong_questions:
        if isinstance(q, dict) and 'exam_type' not in q:
            inferred = infer_exam_type_for_question(q)
            if inferred:
                q = dict(q)
                q['exam_type'] = inferred
        if isinstance(q, dict) and ('difficulty' not in q or not q.get('difficulty')):
            exam_type = q.get('exam_type')
            if exam_type in QUESTION_BANK:
                match = next((qq for qq in QUESTION_BANK[exam_type] if qq.get('id') == q.get('id')), None)
                if match and match.get('difficulty'):
                    q = dict(q)
                    q['difficulty'] = match['difficulty']
        enriched.append(q)
    return render_template('wrong_questions.html', 
                           wrong_questions=enriched,
                           languages=LANGUAGES, 
                           current_language=get_locale())

# 生成同类真题（模拟功能）
@app.route('/similar-questions/<topic>')
def similar_questions(topic):
    # 模拟查找同类真题
    similar_qs = []
    exclude_id = request.args.get('exclude_id', type=int)
    exam_type_filter = request.args.get('exam_type')
    for exam_type, questions in QUESTION_BANK.items():
        if exam_type_filter and exam_type != exam_type_filter:
            continue
        for q in questions:
            if q['topic'] == topic and (exclude_id is None or q.get('id') != exclude_id):
                similar_qs.append(q)
    
    return render_template('similar_questions.html', 
                           topic=topic, 
                           similar_questions=similar_qs,
                           languages=LANGUAGES, 
                           current_language=get_locale())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
