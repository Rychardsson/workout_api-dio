from pydantic import field_validator


def validate_cpf(cpf: str) -> str:
    """
    Valida CPF brasileiro
    Remove caracteres não numéricos e verifica se tem 11 dígitos
    """
    # Remove caracteres não numéricos
    cpf_numbers = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf_numbers) != 11:
        raise ValueError('CPF deve conter exatamente 11 dígitos')
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf_numbers == cpf_numbers[0] * 11:
        raise ValueError('CPF inválido')
    
    # Validação dos dígitos verificadores
    def calculate_digit(cpf_partial: str, weight: int) -> int:
        total = sum(int(digit) * (weight - idx) for idx, digit in enumerate(cpf_partial))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Valida primeiro dígito
    first_digit = calculate_digit(cpf_numbers[:9], 10)
    if first_digit != int(cpf_numbers[9]):
        raise ValueError('CPF inválido')
    
    # Valida segundo dígito
    second_digit = calculate_digit(cpf_numbers[:10], 11)
    if second_digit != int(cpf_numbers[10]):
        raise ValueError('CPF inválido')
    
    return cpf_numbers
