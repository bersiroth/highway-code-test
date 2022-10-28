from dependency_injector import containers, providers

from highway_code.application.question.handler import QuestionHandler
from highway_code.application.statistic.handler import StatisticHandler
from highway_code.domain.question.manager import QuestionManager
from highway_code.domain.question.render import (
    CliRenderQuestion,
    CliRenderQuestionManager,
)
from highway_code.domain.statistic.manager import StatisticManager
from highway_code.domain.statistic.render import CliRenderStatistic
from highway_code.infrastructure.persistence.question import JsonQuestionRepository
from highway_code.infrastructure.persistence.statistic import JsonStatisticRepository
from highway_code.infrastructure.render.cli import ClickCliRender
from highway_code.infrastructure.translation.translation import GettextTranslation


class Container(containers.DeclarativeContainer):
    translation = providers.Factory(GettextTranslation)
    question_repository = providers.Factory(JsonQuestionRepository)
    statistic_repository = providers.Factory(JsonStatisticRepository)
    cli_render = providers.Factory(ClickCliRender)

    cli_render_question_manager = providers.Factory(CliRenderQuestionManager, cli_render=cli_render)
    cli_render_question = providers.Factory(CliRenderQuestion, cli_render=cli_render)
    cli_render_statistic = providers.Factory(CliRenderStatistic, cli_render=cli_render)

    question_manager = providers.Factory(
        QuestionManager,
        question_repository=question_repository,
        translation=translation,
        cli_render_question_manager=cli_render_question_manager,
        cli_render_question=cli_render_question,
    )
    statistic_manager = providers.Factory(
        StatisticManager, statistic_repository=statistic_repository, cli_render_statistic=cli_render_statistic
    )

    question_handler = providers.Factory(
        QuestionHandler, question_manager=question_manager, statistic_manager=statistic_manager
    )
    statistic_handler = providers.Factory(StatisticHandler, statistic_manager=statistic_manager)
